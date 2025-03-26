import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pdf_extractor import extract_text_from_pdf
from model import recommend_jobs

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}

# Check file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)

        # Get job recommendations
        recommendations = recommend_jobs(resume_text)

        return render_template("results.html", jobs=recommendations)

    return "Invalid file format"

if __name__ == "__main__":
    app.run(debug=True)
