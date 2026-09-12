#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import uuid
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from werkzeug.utils import secure_filename

from config import TELEGRAM_BOT_TOKEN, UPLOAD_FOLDER
from services.extractor import extract_text
from services.chatbot import process_candidate


# Maximum number of resumes allowed per analysis
MAX_RESUMES = 10


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start a new resume analysis session.
    """

    # Clear previous session
    context.user_data.clear()

    await update.message.reply_text(
        "🤖 Welcome to AI Resume Analyzer!\n\n"

        "I can compare multiple resumes against one Job Description.\n\n"

        "📌 HOW TO USE\n\n"

        "1️⃣ Send the Job Description as a text message.\n"
        "2️⃣ Upload multiple resumes (PDF, DOCX or TXT).\n"
        "3️⃣ When you finish uploading, send /analyze.\n"
        "4️⃣ I will analyze and rank all candidates.\n\n"

        f"📄 You can upload up to {MAX_RESUMES} resumes.\n\n"

        "The final result includes:\n"
        "📊 ATS Score\n"
        "🏆 Candidate Ranking\n"
        "✅ Matched Skills\n"
        "❌ Missing Skills\n"
        "💪 Strengths\n"
        "⚠️ Weaknesses\n"
        "📚 Recommended Courses\n"
        "📝 Resume Improvements"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Display usage instructions.
    """

    await update.message.reply_text(
        "📌 HOW TO USE THE BOT\n\n"

        "1. Send /start\n"
        "2. Send the Job Description\n"
        "3. Upload Resume 1\n"
        "4. Upload Resume 2\n"
        "5. Upload Resume 3\n"
        "6. Continue uploading resumes\n"
        "7. Send /analyze\n\n"

        f"Maximum resumes: {MAX_RESUMES}\n\n"

        "Supported formats:\n"
        "📄 PDF\n"
        "📄 DOCX\n"
        "📄 TXT"
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancel the current session and delete uploaded files.
    """

    resume_files = context.user_data.get("resumes", [])

    for resume in resume_files:
        file_path = resume.get("path")

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Current analysis session cancelled.\n\n"
        "Send /start to begin again."
    )


async def receive_job_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Receive and store the Job Description.
    """

    job_description = update.message.text.strip()

    if not job_description:
        await update.message.reply_text(
            "❌ Please send a valid Job Description."
        )
        return

    # Store JD
    context.user_data["job_description"] = job_description

    # Create empty resume list
    context.user_data["resumes"] = []

    await update.message.reply_text(
        "✅ Job Description received!\n\n"

        "📄 Now upload your resumes.\n\n"

        f"You can upload up to {MAX_RESUMES} resumes.\n\n"

        "After uploading all resumes, send:\n"
        "/analyze"
    )


async def receive_resume(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Receive and store each resume.
    """

    # Check if Job Description exists
    if "job_description" not in context.user_data:
        await update.message.reply_text(
            "⚠️ Please send the Job Description first.\n\n"
            "Use /start to begin."
        )
        return

    document = update.message.document

    if not document:
        return

    filename = document.file_name or "resume"

    allowed_extensions = (".pdf", ".docx", ".txt")

    if not filename.lower().endswith(allowed_extensions):
        await update.message.reply_text(
            "❌ Unsupported file format.\n\n"
            "Please upload PDF, DOCX or TXT."
        )
        return

    # Get current resumes
    resumes = context.user_data.get("resumes", [])

    # Check maximum number of resumes
    if len(resumes) >= MAX_RESUMES:
        await update.message.reply_text(
            f"⚠️ Maximum limit of {MAX_RESUMES} resumes reached.\n\n"
            "Send /analyze to start the analysis."
        )
        return

    # Create safe filename
    safe_filename = secure_filename(filename)

    unique_filename = (
        f"{uuid.uuid4().hex}_{safe_filename}"
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    try:

        # Download Telegram file
        telegram_file = await document.get_file()

        await telegram_file.download_to_drive(file_path)

        # Add resume to user's session
        resumes.append(
            {
                "filename": filename,
                "path": file_path
            }
        )

        context.user_data["resumes"] = resumes

        resume_number = len(resumes)

        await update.message.reply_text(
            f"✅ Resume {resume_number} received!\n\n"
            f"📄 File: {filename}\n"
            f"📊 Total resumes: {resume_number}/{MAX_RESUMES}\n\n"

            "You can upload another resume or send:\n"
            "/analyze"
        )

    except Exception as error:

        if os.path.exists(file_path):
            os.remove(file_path)

        await update.message.reply_text(
            f"❌ Failed to receive resume.\n\n"
            f"Error: {str(error)}"
        )


async def analyze_resumes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Analyze all uploaded resumes against the same Job Description.
    """

    # Check Job Description
    if "job_description" not in context.user_data:

        await update.message.reply_text(
            "⚠️ Please send the Job Description first.\n\n"
            "Use /start to begin."
        )
        return

    # Get resumes
    resumes = context.user_data.get("resumes", [])

    if not resumes:

        await update.message.reply_text(
            "⚠️ No resumes uploaded yet.\n\n"
            "Please upload at least one resume before "
            "using /analyze."
        )
        return

    # Prevent duplicate analysis
    if context.user_data.get("analyzing", False):

        await update.message.reply_text(
            "⏳ Analysis is already running. Please wait."
        )
        return

    context.user_data["analyzing"] = True

    job_description = context.user_data["job_description"]

    await update.message.reply_text(
        "⏳ ANALYSIS STARTED\n\n"
        f"📄 Resumes received: {len(resumes)}\n"
        "🔍 Extracting resume information...\n"
        "🤖 Running ATS + AI analysis...\n"
        "🏆 Ranking candidates...\n\n"
        "Please wait..."
    )

    results = []

    try:

        # Process each resume
        for index, resume in enumerate(resumes, start=1):

            filename = resume["filename"]
            file_path = resume["path"]

            try:

                # Extract resume text
                resume_text = extract_text(file_path)

                if not resume_text.strip():
                    raise ValueError(
                        "Could not extract text from resume."
                    )

                # Run analysis
                # to_thread prevents blocking Telegram's async loop
                result = await asyncio.to_thread(
                    process_candidate,
                    job_description,
                    resume_text
                )

                result["filename"] = filename
                result["candidate_number"] = index

                results.append(result)

            except Exception as error:

                results.append(
                    {
                        "filename": filename,
                        "candidate_number": index,
                        "error": str(error),
                        "ats_score": 0
                    }
                )

        # Sort candidates by ATS score
        results.sort(
            key=lambda x: x.get("ats_score", 0),
            reverse=True
        )

        # Send ranking
        await send_ranking(update, results)

    except Exception as error:

        await update.message.reply_text(
            "❌ Analysis failed.\n\n"
            f"Error: {str(error)}"
        )

    finally:

        # Delete all uploaded files
        for resume in resumes:

            file_path = resume.get("path")

            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        # Clear session
        context.user_data.clear()


async def send_ranking(
    update: Update,
    results
):
    """
    Send ranked candidate results.
    """

    if not results:

        await update.message.reply_text(
            "❌ No candidate results were generated."
        )

        return

    # -----------------------------
    # Ranking message
    # -----------------------------

    message = "🏆 CANDIDATE RANKING\n\n"

    for rank, result in enumerate(results, start=1):

        filename = result.get(
            "filename",
            "Unknown"
        )

        ats_score = result.get(
            "ats_score",
            0
        )

        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        else:
            medal = f"{rank}."

        message += (
            f"{medal} {filename}\n"
            f"📊 ATS Score: {ats_score}%\n\n"
        )

    await update.message.reply_text(message)

    # -----------------------------
    # Detailed result for each candidate
    # -----------------------------

    for rank, result in enumerate(results, start=1):

        filename = result.get(
            "filename",
            "Unknown"
        )

        if result.get("error"):

            detail_message = (
                f"❌ CANDIDATE {rank}\n\n"
                f"📄 Resume: {filename}\n\n"
                f"Error: {result['error']}"
            )

            await update.message.reply_text(
                detail_message
            )

            continue

        ats_score = result.get(
            "ats_score",
            0
        )

        matched = result.get(
            "matched_skills",
            []
        )

        missing = result.get(
            "missing_skills",
            []
        )

        strengths = result.get(
            "strengths",
            []
        )

        weaknesses = result.get(
            "weaknesses",
            []
        )

        courses = result.get(
            "recommended_courses",
            []
        )

        improvements = result.get(
            "resume_improvements",
            []
        )

        summary = result.get(
            "summary",
            ""
        )

        detail_message = f"""
📄 CANDIDATE {rank}
━━━━━━━━━━━━━━━━━━

📄 Resume:
{filename}

📊 ATS SCORE:
{ats_score}%

📝 SUMMARY:
{summary}

✅ MATCHED SKILLS:
{format_list(matched)}

❌ MISSING SKILLS:
{format_list(missing)}

💪 STRENGTHS:
{format_list(strengths)}

⚠️ WEAKNESSES:
{format_list(weaknesses)}

📚 RECOMMENDED COURSES:
{format_list(courses)}

📝 RESUME IMPROVEMENTS:
{format_list(improvements)}
"""

        # Telegram message limit protection
        if len(detail_message) > 4000:

            detail_message = (
                detail_message[:3950]
                + "\n\n...more results omitted."
            )

        await update.message.reply_text(
            detail_message
        )


def format_list(items):
    """
    Convert list into Telegram-friendly bullet points.
    """

    if not items:
        return "• None identified"

    return "\n".join(
        f"• {str(item)}"
        for item in items[:10]
    )


def main():

    if not TELEGRAM_BOT_TOKEN:

        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing from .env"
        )

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    application = (
        Application
        .builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    application.add_handler(
        CommandHandler(
            "cancel",
            cancel_command
        )
    )

    application.add_handler(
        CommandHandler(
            "analyze",
            analyze_resumes
        )
    )

    # Job Description
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_job_description
        )
    )

    # Resumes
    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            receive_resume
        )
    )

    print("🤖 AI Resume Telegram Bot is running...")
    print(f"📄 Maximum resumes: {MAX_RESUMES}")
    print("Press Ctrl+C to stop.")

    application.run_polling()


if __name__ == "__main__":
    main()

