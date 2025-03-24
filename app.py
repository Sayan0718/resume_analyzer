from flask import Flask, render_template, request, redirect, url_for
import os
from models import extract_text_from_pdf, match_jobs

app = Flask(__name__)
UPLOAD_FOLDER = "resume_data"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "resume" not in request.files:
            return "No file part"

        resume_file = request.files["resume"]
        if resume_file.filename == "":
            return "No selected file"

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
        resume_file.save(file_path)

        # Extract text and match jobs
        resume_text = extract_text_from_pdf(file_path)
        matched_jobs = match_jobs(resume_text)

        return render_template("results.html", matched_jobs=matched_jobs)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)