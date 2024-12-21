# ai/models.py
import os
import pickle
from db.queries import get_connection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords

MODEL_PATH = 'model.pkl'

def train_model(db_path='notes.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    c.execute("SELECT text, category FROM notes WHERE category IS NOT NULL AND category <> ''")
    data = c.fetchall()
    conn.close()
    if not data:
        return None

    texts, categories = zip(*data)
    unique_categories = set(categories)
    if len(unique_categories) < 2:
        # Non abbastanza classi differenti
        return None

    # Carichiamo le stopwords italiane da NLTK
    it_stopwords = stopwords.words('italian')

    vectorizer = CountVectorizer(stop_words=it_stopwords)
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression(max_iter=1000)
    model.fit(X, categories)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump((vectorizer, model), f)

    return MODEL_PATH

def suggest_category(text):
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        vectorizer, model = pickle.load(f)
    X = vectorizer.transform([text])
    pred = model.predict(X)
    return pred[0]

