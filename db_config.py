import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",       # Change this if needed
    password="Sayan@0811",       # Change this if needed
    database="resume_analyzer"
)
cursor = db.cursor()
