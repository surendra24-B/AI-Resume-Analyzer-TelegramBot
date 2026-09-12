#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from google import genai

from config import GEMINI_API_KEY


def get_client():

    if not GEMINI_API_KEY:
        raise ValueError(
            "Gemini API key was not found.\n\n"
            "Please add GEMINI_API_KEY to your .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def analyze_resume(job_description, resume_text):

    client = get_client()

    prompt = f"""
You are an expert ATS resume analyzer and technical recruiter.

Analyze the candidate's resume against the given job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

IMPORTANT RULES:
1. Only use information actually present in the resume.
2. Do not invent skills, experience, education or projects.
3. Clearly identify gaps between the resume and job description.
4. Return ONLY valid JSON.
5. Keep the response concise and useful.

Return this exact JSON structure:

{{
    "candidate_name": "",
    "summary": "",
    "matched_skills": [],
    "missing_skills": [],
    "experience_gaps": [],
    "education_match": "",
    "strengths": [],
    "weaknesses": [],
    "resume_improvements": [],
    "recommended_courses": []
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "candidate_name": "",
            "summary": response_text,
            "matched_skills": [],
            "missing_skills": [],
            "experience_gaps": [],
            "education_match": "",
            "strengths": [],
            "weaknesses": [],
            "resume_improvements": [],
            "recommended_courses": []
        }

