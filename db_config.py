import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Sayan@0811",  # Replace with your actual password
    "database": "resume_analyzer"
}

# Function to establish database connection
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("✅ Database connected successfully!")
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
        return None
