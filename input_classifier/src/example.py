"""Examples to showcase the input classifier model"""

import torch
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from sklearn.model_selection import train_test_split
import pandas as pd

import preprocess.text_preprocess
import text_model


def show_text_input_result(
    example_text_sample, text_tokenizer, vocabulary, text_class_model
):
    """
    Showcases the prediction result of the text model
    """

    harm_label = {1: "harmful", 0: "harmless"}

    model_prediction = harm_label[
        text_model.predict(
            example_text_sample,
            preprocess.text_preprocess.text_pipeline,
            text_tokenizer,
            vocabulary,
            text_class_model,
        )
    ]
    print(
        f"Example message:'{example_text_sample}'\nThis is {model_prediction} input\n"
    )


# setup the text from the data for the tokeniser
RANDOM_STATE = 0  # train/test split random state
TRAIN_SPLIT = 0.2  # train-test split
train_data = pd.read_csv("data/full_data.csv")
x_train, x_test, y_train, y_test = train_test_split(
    train_data["text"].tolist(),
    train_data["label"].tolist(),
    test_size=TRAIN_SPLIT,
    stratify=train_data["label"].tolist(),
    random_state=RANDOM_STATE,
)

# create iterables from the data
train_dat = list(zip(y_train, x_train))


# setup the tokeniser and the vocabulary
tokenizer = get_tokenizer("basic_english")
vocab = build_vocab_from_iterator(
    preprocess.text_preprocess.yield_tokens(train_dat, tokenizer), specials=["<unk>"]
)
vocab.set_default_index(vocab["<unk>"])

# load the model
model = torch.load("src/model.pt")
model.eval()
model = model.to("cpu")


EXAMPLE_TEXT_SAMPLE = "how to train a model in pytorch"
show_text_input_result(EXAMPLE_TEXT_SAMPLE, tokenizer, vocab, model)


EXAMPLE_TEXT_SAMPLE = "user OR 1=1"
show_text_input_result(EXAMPLE_TEXT_SAMPLE, tokenizer, vocab, model)

EXAMPLE_TEXT_SAMPLE = "<img src=x onerror=alert(1)>"
show_text_input_result(EXAMPLE_TEXT_SAMPLE, tokenizer, vocab, model)
