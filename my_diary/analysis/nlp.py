# analysis/nlp.py
import nltk
from nltk.corpus import stopwords
import string

def extract_keywords(text, language='italian'):
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words(language))
    keywords = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    return keywords
