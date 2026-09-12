#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pypdf import PdfReader
from docx import Document


def extract_pdf(path):
    """Extract text from a PDF file."""

    reader = PdfReader(path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def extract_docx(path):
    """Extract text from a DOCX file."""

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def extract_txt(path):
    """Extract text from a TXT file."""

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text(path):
    """Automatically detect file type and extract text."""

    path_lower = path.lower()

    if path_lower.endswith(".pdf"):
        return extract_pdf(path)

    if path_lower.endswith(".docx"):
        return extract_docx(path)

    if path_lower.endswith(".txt"):
        return extract_txt(path)

    raise ValueError(
        "Unsupported file format. "
        "Only PDF, DOCX and TXT are supported."
    )

