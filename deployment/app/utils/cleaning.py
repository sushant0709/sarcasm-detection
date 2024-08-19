"""
Cleaning Module
This module defines functions for cleaning text data, including removing features, non-ASCII characters,
lemmatization, and removing stop words.

Functions:
    remove_features(data_str: str) -> str: Removes punctuation, numbers, and non-alphanumeric characters from text.
    rem_non_ascii(data: str) -> str: Removes non-ASCII characters from text.
    lemmatize_sentence(text: str) -> str: Lemmatizes words in a given sentence.
    remove_stops(data_str: str) -> str: Removes stop words from text.
"""

import re
import nltk
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.corpus import wordnet
nltk.download("punkt")
nltk.download("stopwords")
from nltk.corpus import stopwords

def remove_features(data_str):
    """
    Removes punctuation, numbers, and non-alphanumeric characters from the input text.

    Args:
        data_str (str): The input text to be cleaned.

    Returns:
        str: Cleaned text with features removed.
    """
    punc_re = re.compile('[%s]' % re.escape(string.punctuation))
    num_re = re.compile('(\\d+)')
    alpha_num_re = re.compile("^[a-z0-9_.]+$")
    data_str = data_str.lower()
    data_str = punc_re.sub(' ', data_str)
    data_str = num_re.sub(' ', data_str)
    cleaned_str = ' '.join([word for word in data_str.split() if alpha_num_re.match(word) and len(word) > 1])
    return " ".join(cleaned_str.split())

def rem_non_ascii(data):
    """
    Removes non-ASCII characters from the input text.

    Args:
        data (str): The input text.

    Returns:
        str: Text with non-ASCII characters removed.
    """
    return ''.join(c for c in data if 0 < ord(c) < 127)

lemmatizer = WordNetLemmatizer()

def nltk2wn_tag(nltk_tag):
    """
    Maps NLTK POS tags to WordNet POS tags.

    Args:
        nltk_tag (str): The NLTK POS tag.

    Returns:
        str: The corresponding WordNet POS tag.
    """
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def lemmatize_sentence(text):
    """
    Lemmatizes words in a given sentence.

    Args:
        text (str): The input sentence.

    Returns:
        str: The lemmatized sentence.
    """
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(text))
    wn_tagged = map(lambda x: (x[0], nltk2wn_tag(x[1])), nltk_tagged)
    res_words = [lemmatizer.lemmatize(word, tag) if tag is not None else word for word, tag in wn_tagged]
    return " ".join(res_words)

def remove_stops(data_str):
    """
    Removes stop words from the input text.

    Args:
        data_str (str): The input text.

    Returns:
        str: Text with stop words removed.
    """
    stops = set(stopwords.words("english"))
    return ' '.join([word for word in data_str.split() if word not in stops])
