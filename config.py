#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

UPLOAD_FOLDER = str(BASE_DIR / "uploads")

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

MAX_FILE_SIZE = 10 * 1024 * 1024

