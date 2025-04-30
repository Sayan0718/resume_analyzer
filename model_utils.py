# TF-IDF, Cosine similarity and ATS scoring
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess_text
from database_config import db

def fetch_jobs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT job_title, required_skills FROM job_listings")
    jobs = cursor.fetchall()
    return pd.DataFrame(jobs)

def recommend_jobs(resume_text):
    jobs_df = fetch_jobs()
    jobs_df['processed_skills'] = jobs_df['required_skills'].apply(preprocess_text)

    tfidf = TfidfVectorizer()
    job_vectors = tfidf.fit_transform(jobs_df['processed_skills'])

    resume_vector = tfidf.transform([preprocess_text(resume_text)])
    similarities = cosine_similarity(resume_vector, job_vectors).flatten()

    jobs_df["similarity"] = (similarities * 100).round(2)
    top_jobs = jobs_df.sort_values("similarity", ascending=False).head(5)

    return top_jobs[['job_title', 'similarity']].to_dict('records')

def calculate_ats_score(resume_text, job_description):
    resume_text = preprocess_text(resume_text)
    job_description = preprocess_text(job_description)

    resume_words = set(resume_text.split())
    job_words = set(job_description.split())

    matched_words = resume_words.intersection(job_words)
    missing_words = job_words.difference(resume_words)

    score = (len(matched_words) / len(job_words)) * 100 if job_words else 0

    return round(score, 2), list(missing_words)

def suggest_improvements(resume_text):
    # Simple logic to simulate improvement suggestions
    required_keywords = ["teamwork", "communication", "python", "sql", "leadership", "problem-solving"]
    resume_words = preprocess_text(resume_text).split()

    missing = [word.capitalize() for word in required_keywords if word.lower() not in resume_words]
    return missing