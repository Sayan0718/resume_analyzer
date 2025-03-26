CREATE DATABASE IF NOT EXISTS resume_analyzer;
USE resume_analyzer;

CREATE TABLE IF NOT EXISTS job_listings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255),
    job_description TEXT,
    required_skills TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    resume_path VARCHAR(255)
);
