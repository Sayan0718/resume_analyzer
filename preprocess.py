import nltk
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure stopwords are downloaded (run only once)
nltk.download("stopwords")
from nltk.corpus import stopwords

# Text preprocessing function clearly defined
def preprocess_text(text):
    text = text.lower()  # convert text to lowercase
    text = re.sub(r'\d+', '', text)  # remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    text = " ".join([word for word in text.split() if word not in stopwords.words("english")])  # remove stopwords
    return text

# Function to create TF-IDF vectors for job skills
def vectorize_jobs(job_data):
    job_data["processed_skills"] = job_data["required_skills"].apply(preprocess_text)
    tfidf = TfidfVectorizer()
    job_vectors = tfidf.fit_transform(job_data["processed_skills"])
    return tfidf, job_vectors
