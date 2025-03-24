import os
import fitz  # PyMuPDF for extracting text from PDFs
import mysql.connector
from db_config import create_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Function to extract text from PDF resume
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text


# Function to fetch job listings from the database
def get_job_data():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, job_title, required_skills FROM job_listings")
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jobs
    return []


# Function to match resume with jobs based on required skills
def match_jobs(resume_text):
    job_data = get_job_data()
    required_skills = [job["required_skills"] for job in job_data]

    if not required_skills:
        return []

    vectorizer = TfidfVectorizer()
    skill_vectors = vectorizer.fit_transform(required_skills)  # Skills from jobs
    resume_vector = vectorizer.transform([resume_text])  # Resume content

    similarity_scores = cosine_similarity(resume_vector, skill_vectors)[0]
    matched_jobs = sorted(
        zip(job_data, similarity_scores),
        key=lambda x: x[1],
        reverse=True
    )

    return matched_jobs[:5]  # Return top 5 job matches
