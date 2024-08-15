"""pytorch batching functionality"""

from typing import Callable, Generator

import torch
import torchtext.vocab

import preprocess.text_preprocess as tp


def collate_batch(
    batch: Generator,
    tokenizer: Callable,
    vocab: torchtext.vocab.Vocab,
    device: str = "cpu",
):
    """
    Dataloader `collate_fn` funtion input that creates tensors from the batches' data,
    labels and offsets and pushes them to the selectd device

    Parameters
    ----------
    batch : Generator
        Input data segmented into batches for further processing
    tokenizer : Callable
        Tokenizer function
    vocab : torchtext.vocab.Vocab
        A `Vocab` object
    device : str
        The device the computation is sent to
    """

    label_list, text_list, offsets = [], [], [0]
    for _label, _text in batch:
        label_list.append(tp.label_pipeline(_label))
        processed_text = torch.tensor(
            tp.text_pipeline(_text, tokenizer, vocab), dtype=torch.int64
        )
        text_list.append(processed_text)
        offsets.append(processed_text.size(0))
    label_list = torch.tensor(label_list, dtype=torch.int64)
    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    text_list = torch.cat(text_list)
    return label_list.to(device), text_list.to(device), offsets.to(device)
