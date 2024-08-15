"""Text preprocessing to prepare the data for usage in a model"""

from typing import Callable, Generator, Union
import torchtext.vocab


def yield_tokens(data_iter: list, tokenizer: Callable) -> Generator:
    """
    Creates an generator from a given iterable data structure, containing the tokenized text

    Parameters:
    -----------
    data_iter : list (or list-like)
        Iterable data structure containing the data
    tokenizer : Callable
        Tokenization function

    Returns:
    --------
    token : Generator
        The output generator
    """
    for _, text in data_iter:
        yield tokenizer(text)


def text_pipeline(
    text: str, tokenizer: Callable, vocab: torchtext.vocab.Vocab
) -> list[int]:
    """
    Tokenizes the text input and subsequently obtains the corresponding text's index

    Parameters
    ----------
    text : str
        Text to be converted into its corresponding indexes
    tokenizer : Callable
        Tokeniser function
    vocab : torchtext.vocab.Vocab
        A `Vocab` object

    Returns:
    --------
    indexes : list[int]
        List containing the input text's indexes
    """

    return vocab(tokenizer(text))


def label_pipeline(label: Union[int, str]) -> int:
    """
    Turns the input data labels into integers


    Parameters:
    -----------
    label : Union[int, str]
        Input label

    Returns:
    --------
    int_label : int
        Input label after being converted into an integer

    """
    return int(label)
