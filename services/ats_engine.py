#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re


SKILLS = {
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",

    "html",
    "css",
    "react",
    "angular",
    "vue",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",

    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",

    "flask",
    "django",
    "fastapi",

    "rest api",
    "api",

    "git",
    "github",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "linux",
    "data structures",
    "algorithms",

    "power bi",
    "tableau",

    "excel"
}


def normalize_text(text):
    """Normalize text for matching."""

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    """Extract known technical skills from text."""

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(found_skills)


def calculate_skill_score(resume_skills, jd_skills):
    """Calculate percentage of required skills found."""

    if not jd_skills:
        return 0

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set.intersection(jd_set)

    score = (len(matched) / len(jd_set)) * 100

    return round(score, 2)


def get_matched_skills(resume_skills, jd_skills):
    """Return skills present in both JD and resume."""

    return sorted(
        set(resume_skills).intersection(set(jd_skills))
    )


def get_missing_skills(resume_skills, jd_skills):
    """Return JD skills missing from resume."""

    return sorted(
        set(jd_skills) - set(resume_skills)
    )


def calculate_keyword_score(resume, job_description):
    """
    Basic keyword similarity score.

    This is intentionally simple because semantic
    understanding is handled by the AI analyzer.
    """

    resume_words = set(
        normalize_text(resume).split()
    )

    jd_words = set(
        normalize_text(job_description).split()
    )

    if not jd_words:
        return 0

    common_words = resume_words.intersection(jd_words)

    score = len(common_words) / len(jd_words) * 100

    return round(min(score, 100), 2)


def calculate_ats_score(
    skill_score,
    experience_score=75,
    education_score=80,
    keyword_score=70,
    quality_score=80
):
    """
    Calculate final ATS score.

    Weight:
    Skills       = 40%
    Experience   = 25%
    Education    = 15%
    Keywords     = 10%
    Quality      = 10%
    """

    score = (
        skill_score * 0.40
        + experience_score * 0.25
        + education_score * 0.15
        + keyword_score * 0.10
        + quality_score * 0.10
    )

    return round(score, 2)

