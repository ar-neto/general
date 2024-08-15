# Input validator

## Introduction & motivation
When it comes to cyber-security, be it for search queries on search bars, a text input on a password field or text on user generated content, the need to make sure text added by users in a platform is harmless to it. If such assurance isn't provided, that can leave platforms vulnerable to all sorts of malicious attacks (for instance [cross-site scripting (XSS)](https://portswigger.net/web-security/cross-site-scripting) and [SQL injection (SQLI)](https://portswigger.net/web-security/sql-injection)), which in turn can lead to disastrous consequences, such as data exfiltration or tampering, unauthorised login and more.
So, prevent this, different approaches can be taken. Often times, user input is validated, filtered and sanitised before it is processed in order to make sure it's completely harmless. This way, whether it's text on a comment section or on an uploaded user file, it is stil possible to ensure the input is not going to damage any platforms or its underlying assets.
As such, in addition to all other methods to validate text input, this project adds yet another way to do so: via [NLP](https://www.oracle.com/pt/artificial-intelligence/what-is-natural-language-processing/) - more specifically, through text classification.

## The idea & architecture
The goal here is to build a text classification model that is able to distinguish between regular text, that would normally be regarded as legitimate input (hereafter referred as harmful text), and text that is meant for malicious purposes (from here on out regarded as harmful text). That distinction will be made by a model with a simple architecture, as shown below:

```
TextClassificationModel(
  (embedding): EmbeddingBag(16418, 128, mode='mean')
  (fc1): Linear(in_features=128, out_features=64, bias=True)
  (fc2): Linear(in_features=64, out_features=16, bias=True)
  (fc3): Linear(in_features=16, out_features=2, bias=True)
)
```


## Training/testing & validation Data
The examples labelled as `harmless` were obtained from the ["Tab-delimited Bilingual Sentence Pairs"](https://www.manythings.org/anki/) from the [Tatoeba project](http://tatoeba.org/home). The original data can be found [here](https://www.manythings.org/anki/deu-eng.zip).

Now, the examples labelled as `harmful` were obtained from both an [SQLI wordlist](https://github.com/payloadbox/sql-injection-payload-list) by the github user [Payload box](https://github.com/payloadbox) and a [XSS wordlist](https://github.com/payloadbox/xss-payload-list) made by the user [Payload Box](https://github.com/payloadbox). The filtered and labelled dataset for train/testing and validation can be found in the `data` folder under the names `full_data.csv` and `validation.csv`, respectively. 

When it comes to labels, the data has two labels: `harmful` (one-hot encoded into the number `1`) and `harmless` (one-hot encoded as `0`). The data's distribution is as follows:

Train/test data:
----------------
Number of samples: 196887
Number of harmful text samples: 2363 (~1.2% of the total dataset)
Number of harmless text samples: 194524


Validation data:
----------------
Number of samples: 84380
Number of harmful text samples: 1013 (~1.2% of the total dataset)
Number of harmless text samples: 83367

## Preprocessing
The data needs to be converted into a representation that computers can understand. For that, the wordlists mentioned above, were aggregated into one labelled dataset - this process can be found in `src/preprocess/prepare_datasets.py`. Afterwards, that dataset was both tokenised and a vocabulary was created from it. Here, the model also had an embedding layer that mapped the data into a vector space, thus achieving a representation that the subsequent layers could understand.

## Results and examples
As for results, via 3 epochs alone this model was able to obtain a **validation accuracy of over 90%**, as shown below in the model training logs. Such accuracy can be attributed to the selected wordlists for the harmful text being so starkingly different from the harmless text strings.

`| end of epoch 3 | time: 89.98933410644531s | valid accuracy 0.9998696373548234 `

# Examples

Below, logs of examples of the model's usage on arbitrary input is shown, as generated from `src/example.py`:

```
Example message:'how to train a model in pytorch'
This is harmless input

Example message:'user OR 1=1'
This is harmful input

Example message:'<img src=x onerror=alert(1)>'
This is harmful input
```
