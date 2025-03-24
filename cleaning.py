import pandas as pd

# Load the CSV file (make sure the filename is correct)
df = pd.read_csv("D:/resume-analyzer/jobs.csv")

# Ensure column names are correct (print column names to verify)
print("Columns in dataset:", df.columns)

# Rename columns if they have extra spaces or incorrect names
df.columns = df.columns.str.strip().str.lower()  # Convert column names to lowercase & remove spaces
df.rename(columns={"job title": "job title", "key skills": "key skills"}, inplace=True)

# Check if required columns exist
if "job title" not in df.columns or "key skills" not in df.columns:
    raise ValueError("Columns 'job title' or 'key skills' not found in the dataset!")

# Group by 'job_title' and merge 'required_skills' using a newline for readability
df_grouped = df.groupby("job title")["key skills"].apply(lambda x: '\n- '.join(x.unique())).reset_index()

# Add bullet points for better readability
df_grouped["key skills"] = "- " + df_grouped["key skills"]

# Save cleaned data to a new CSV file
df_grouped.to_csv("cleaned_jobs.csv", index=False)

print("✅ Data cleaned! Duplicate job titles merged successfully.")
