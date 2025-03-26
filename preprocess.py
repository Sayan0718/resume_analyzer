import nltk
import string
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("stopwords")
from nltk.corpus import stopwords

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = " ".join([word for word in text.split() if word not in stopwords.words("english")])  # Remove stopwords
    return text

# Function to transform job descriptions using TF-IDF
def vectorize_jobs(job_data):
    job_data["processed_skills"] = job_data["required_skills"].apply(preprocess_text)
    tfidf = TfidfVectorizer()
    job_vectors = tfidf.fit_transform(job_data["processed_skills"])
    return tfidf, job_vectors
