#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import uuid

from flask import (
    Flask,
    render_template,
    request
)

from werkzeug.utils import secure_filename

from config import (
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS
)

from services.extractor import extract_text

from services.chatbot import (
    process_candidate
)


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = (
        filename.rsplit(".", 1)[1]
        .lower()
    )

    return extension in ALLOWED_EXTENSIONS


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    job_description = (
        request.form
        .get("job_description", "")
        .strip()
    )

    files = request.files.getlist(
        "resumes"
    )

    if not job_description:

        return render_template(
            "index.html",
            error="Please enter a job description."
        )

    if not files:

        return render_template(
            "index.html",
            error="Please upload at least one resume."
        )

    results = []

    for file in files:

        if not file.filename:
            continue

        if not allowed_file(
            file.filename
        ):

            continue

        original_filename = secure_filename(
            file.filename
        )

        unique_filename = (
            f"{uuid.uuid4().hex}_"
            f"{original_filename}"
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        try:

            file.save(file_path)

            resume_text = extract_text(
                file_path
            )

            if not resume_text.strip():

                raise ValueError(
                    "Could not extract text from resume."
                )

            analysis = process_candidate(
                job_description,
                resume_text
            )

            analysis[
                "filename"
            ] = original_filename

            results.append(
                analysis
            )

        except Exception as error:

            results.append({

                "filename":
                    original_filename,

                "error":
                    str(error)

            })

        finally:

            # Delete uploaded file after processing
            if os.path.exists(
                file_path
            ):

                os.remove(
                    file_path
                )

    # Highest ATS score first
    results.sort(
        key=lambda x:
            x.get("ats_score", 0),
        reverse=True
    )

    return render_template(
        "index.html",
        results=results
    )


@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum size is 10 MB."
    ), 413


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )

