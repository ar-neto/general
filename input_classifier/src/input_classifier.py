"""input classifier implementation"""

import time
from functools import partial

import pandas as pd
import torch
from torch.utils.data import DataLoader
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from sklearn.model_selection import train_test_split

import preprocess.text_preprocess
import batching
import text_model

# tutorial: https://www.youtube.com/watch?v=8gAUjBi330gtorch.__version__
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Tokenize the text data

train_data = pd.read_csv("data/full_data.csv")
validation_data = pd.read_csv("data/validation_data.csv")

RANDOM_STATE = 0  # train/test split random state
TRAIN_SPLIT = 0.2  # train-test split

# train/test split
x_train, x_test, y_train, y_test = train_test_split(
    train_data["text"].tolist(),
    train_data["label"].tolist(),
    test_size=TRAIN_SPLIT,
    stratify=train_data["label"].tolist(),
    random_state=RANDOM_STATE,
)

# create iterables from the data
train_dat = list(zip(y_train, x_train))
test_dat = list(zip(y_test, x_test))
valid_dat = list(
    zip(validation_data["label"].tolist(), validation_data["text"].tolist())
)

tokenizer = get_tokenizer("basic_english")
vocab = build_vocab_from_iterator(
    preprocess.text_preprocess.yield_tokens(train_dat, tokenizer), specials=["<unk>"]
)
# handles unknown words
vocab.set_default_index(vocab["<unk>"])


num_class = len({label for (label, _) in train_dat})
vocab_size = len(vocab)
EMBEDDING_SIZE = 128  # embeding size
MODEL = text_model.TextClassificationModel(vocab_size, EMBEDDING_SIZE, num_class).to(
    device
)

# Hyperparameters
EPOCHS = 3  # number of epochs
LR = 10  # learning rate
BATCH_SIZE = 16  # training batch size

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(MODEL.parameters(), lr=LR)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1.0, gamma=0.1)
TOTAL_ACCU = None


train_dataloader = DataLoader(
    train_dat,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=partial(
        batching.collate_batch, tokenizer=tokenizer, vocab=vocab, device=device
    ),
)
valid_dataloader = DataLoader(
    valid_dat,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=partial(
        batching.collate_batch, tokenizer=tokenizer, vocab=vocab, device=device
    ),
)
test_dataloader = DataLoader(
    test_dat,
    batch_size=BATCH_SIZE,
    shuffle=True,
    collate_fn=partial(
        batching.collate_batch, tokenizer=tokenizer, vocab=vocab, device=device
    ),
)

for epoch in range(1, EPOCHS + 1):
    epoch_start_time = time.time()
    text_model.train(train_dataloader, MODEL, optimizer, criterion, epoch)
    accu_val = text_model.evaluate(valid_dataloader, MODEL)
    if TOTAL_ACCU is not None and TOTAL_ACCU > accu_val:
        scheduler.step()
    else:
        TOTAL_ACCU = accu_val
    print("-" * 59)
    print(
        f"| end of epoch {epoch} | time: {time.time() - epoch_start_time}s |\
 valid accuracy {accu_val} "
    )
    print("-" * 59)

print("Checking the results of test dataset.")
accu_test = text_model.evaluate(test_dataloader, MODEL)
print(f"test accuracy {accu_test}")

harm_label = {1: "harmful", 0: "harmless"}
EXAMPLE_TEXT_SAMPLE = "how to train a model in pytorch"
model = MODEL.to("cpu")

# save the model
torch.save(model, "src/model.pt")

text_prediction = harm_label[
    text_model.predict(
        EXAMPLE_TEXT_SAMPLE,
        preprocess.text_preprocess.text_pipeline,
        tokenizer,
        vocab,
        model,
    )
]
print(
    f"Test message:'{EXAMPLE_TEXT_SAMPLE}'\nThis is \
{text_prediction}\
 input"
)
