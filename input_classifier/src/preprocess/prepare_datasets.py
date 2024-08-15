"""Script detailing how the data was obtained and labelled"""

import copy

import pandas as pd


# prepare the harmless text data
def load_data(file_path: str, encoding: str = "UTF-8"):
    """
    Loads the contents of the desired filepath into a variable

    Parameters:
    -----------
    file_path : str
        FIle path to the desired file
    encoding : str
        Desired character encoding

    Returns:
    --------
    file : list
        File contents, where each list item corresponds to one file line

    """

    with open(file_path, encoding=encoding) as f:
        file = f.readlines()

    return file


def show_label_fraction(data, data_name: str = "Data"):
    """
    Shows the data labels' fraction to the entire dataset
    """

    num_data = len(data)
    num_harmful_data = len(data[data["label"] == 1])
    num_harmless_data = len(data[data["label"] == 0])
    print(
        f"""\n{data_name}:
Number of samples: {num_data}
Number of harmful text samples: {num_harmful_data} \
(~{round(num_harmful_data / num_data, 3) * 100}% of the total dataset)
Number of harmless text samples: {num_harmless_data}
"""
    )


harmless_file_path = "data/harmless_text/deu-eng/deu.txt"
harmless_file = load_data(
    harmless_file_path
)  # data source: https://www.manythings.org/anki/deu-eng.zip

# only the english sentences were kept in this dataset
harmless_file = [line.split("\t")[0] for line in harmless_file]
harmless_df = pd.DataFrame(harmless_file)  # the data was made into a dataframe
harmless_df["label"] = 0  # the are the harmless examples and are labelled accordingly
harmless_df.rename(columns={0: "text"}, inplace=True)  # the text columns was renamed

# showcase the data
print(f"Harmless data sample:\n{harmless_df.head()}\n")

# harmful data (SQLI strings)
sqli_harmful_data = load_data(
    "data/harmful_text/sqli_list.txt"
)  # data source: https://github.com/payloadbox/sql-injection-payload-list

# remove trailing newline characters
sqli_harmful_data = [line.strip("\n") for line in sqli_harmful_data]
sqli_harmful_df = pd.DataFrame(sqli_harmful_data)

# harmful data (XSS strings)
xss_harmful_data = load_data("data/harmful_text/xss_list.txt")
xss_harmful_data = [line.strip("\n") for line in xss_harmful_data]
xss_harmful_df = pd.DataFrame(xss_harmful_data)

# join both sources of harmful data
harmful_df = pd.concat([sqli_harmful_df, xss_harmful_df])
harmful_df["label"] = 1
harmful_df.rename(columns={0: "text"}, inplace=True)
print(f"Harmful data sample:\n{harmful_df.head()}\n")

# contatenate everything into one dataset and export
full_data = pd.concat([harmless_df, harmful_df])
full_data = full_data.reset_index(level=0, drop=True)
full_data.index.rename("id", inplace=True)

# random sample of 50% of each class
validation_data = full_data.groupby("label").sample(frac=0.3, random_state=0)
full_data = copy.deepcopy(full_data).drop(validation_data.index)

# export the data into files
print(f"Full data sample:\n{full_data.head()}")


show_label_fraction(full_data, "Train/test data")
full_data.to_csv("data/full_data.csv")

show_label_fraction(validation_data, "Validation data")
validation_data.to_csv("data/validation_data.csv")

# train/test data without labels
full_data_no_labels = full_data["text"]
full_data_no_labels.to_csv("data/full_data_no_labels.csv", index=False)
