"""Text model implementation and arquitecture"""

import time
from typing import Callable

import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchtext.vocab


class TextClassificationModel(nn.Module):
    """
    Text classification model

    Parameters:
    -----------
    vocab_size : int
        Vocabulary size to be learned
    embed_dim : int
        Embedding dimension size
    num_class : int
        Number of classes for the classification task


    """

    def __init__(self, vocab_size, embed_dim, num_class):
        super(TextClassificationModel, self).__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=False)
        self.fc1 = nn.Linear(embed_dim, 64)
        self.fc2 = nn.Linear(64, 16)
        self.fc3 = nn.Linear(16, num_class)
        self.init_weights()

    def init_weights(self):
        """Weights and biases« initialisation"""
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc1.weight.data.uniform_(-initrange, initrange)
        self.fc1.bias.data.zero_()
        self.fc2.weight.data.uniform_(-initrange, initrange)
        self.fc2.bias.data.zero_()
        self.fc3.weight.data.uniform_(-initrange, initrange)
        self.fc3.bias.data.zero_()

    def forward(self, text: torch.Tensor, offsets: torch.Tensor) -> float:
        """
        Forward propagation routine

        Parameters:
        -----------
        text : torch.Tensor
            torch.Tensor containing the text sample
        offsets : torch.Tensor
            torch.Tensor containing the offset - which in this case corresponds to the text size

        Returns:
        --------
        x : float
            output of the model's forward propagation

        """
        embedded = self.embedding(text, offsets)
        x = F.relu(self.fc1(embedded))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train(
    dataloader: DataLoader,
    model: TextClassificationModel,
    optimizer: torch.optim,
    criterion: torch.optim.lr_scheduler,
    epoch: int,
) -> None:
    """
    Model training routine

    Parameters:
    -----------
    dataloader : DataLoader
        Data loader. Combines a dataset and a sampler, and provides an
        iterable over the given dataset
    model : TextClassificationModel
        Text classification model
    optimizer : torch.optim
        Optimization algorithms from Pytorch
    criterion : torch.optim.lr_scheduler
        Learning scheduler from pytorch
    epoch : int
        Number of training epochs
    """
    model.train()
    total_acc, total_count = 0, 0
    log_interval = 500
    start_time = time.time()

    for idx, (label, text, offsets) in enumerate(dataloader):
        optimizer.zero_grad()
        predited_label = model(text, offsets)
        loss = criterion(predited_label, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
        optimizer.step()
        total_acc += (predited_label.argmax(1) == label).sum().item()
        total_count += label.size(0)
        if idx % log_interval == 0 and idx > 0:
            elapsed = time.time() - start_time
            print(
                f"| epoch {epoch} | {idx}/{len(dataloader)} batches | accuracy \
{total_acc / total_count} | time elapled: {elapsed}"
            )
            total_acc, total_count = 0, 0
            start_time = time.time()


def evaluate(dataloader: DataLoader, model: TextClassificationModel):
    """
    Model evaluation routine

    Parameters:
    -----------
    dataloader : DataLoader
        Data loader. Combines a dataset and a sampler, and provides an \
            iterable over the given dataset.
    model : TextClassificationModel
        Text classification model

    """
    model.eval()
    total_acc, total_count = 0, 0

    with torch.no_grad():
        for label, text, offsets in dataloader:
            predited_label = model(text, offsets)
            # loss = criterion(predited_label, label)
            total_acc += (predited_label.argmax(1) == label).sum().item()
            total_count += label.size(0)
    return total_acc / total_count


def predict(
    text: str,
    text_pipeline: Callable,
    tokenizer: Callable,
    vocab: torchtext.vocab.Vocab,
    model: TextClassificationModel,
):
    """
    Model prediction routine

    Paramters:
    ----------
    text : str
        Text sanple that will be sued for prediction
    tokenizer : Callable
        Tokeniser function
    vocab : torchtext.vocab.Vocab
        A `Vocab` object
    model : TextClassificationModel
        Text classification model

    Returns:
    --------
    class : int
        Integer representing the text sample's predicted class
    """

    with torch.no_grad():
        text = torch.tensor(text_pipeline(text, tokenizer, vocab))
        output = model(text, torch.tensor([0]))
        return output.argmax(1).item()
