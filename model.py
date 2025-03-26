import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess_text, vectorize_jobs
from db_config import db


# Load job data from MySQL
def fetch_jobs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT job_title, required_skills FROM job_listings")
    jobs = cursor.fetchall()
    return pd.DataFrame(jobs)


# Function to recommend jobs based on resume
def recommend_jobs(resume_text):
    jobs_df = fetch_jobs()

    if jobs_df.empty:
        return []

    tfidf, job_vectors = vectorize_jobs(jobs_df)

    # Process resume and vectorize it
    processed_resume = preprocess_text(resume_text)
    resume_vector = tfidf.transform([processed_resume])

    # Compute cosine similarity
    similarities = cosine_similarity(resume_vector, job_vectors).flatten()

    # Convert similarity to percentage
    similarities = (similarities * 100).round(2)

    # Get top 5 matching jobs
    jobs_df["similarity"] = similarities
    recommended_jobs = jobs_df.sort_values(by="similarity", ascending=False).head(5)

    return recommended_jobs[["job_title", "similarity"]].to_dict(orient="records")
