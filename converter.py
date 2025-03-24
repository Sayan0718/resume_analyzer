import pandas as pd
import mysql.connector
from db_config import create_connection  # Importing your existing DB connection function

# Step 1: Load the CSV file
csv_file = "D:/resume-analyzer/jobs.csv"  # Update with the correct file path
df = pd.read_csv(csv_file)

# Step 2: Establish Database Connection
conn = create_connection()
cursor = conn.cursor()

# Step 3: Insert Data into MySQL Table
for index, row in df.iterrows():
    job_title = row["Job Title"]
    required_skills = row["Key Skills"]

    sql = "INSERT INTO job_listings (job_title, required_skills) VALUES (%s, %s)"
    values = (job_title, required_skills)

    cursor.execute(sql, values)

# Step 4: Commit and Close Connection
conn.commit()
cursor.close()
conn.close()

print("✅ CSV data uploaded successfully!")
