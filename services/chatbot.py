#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from services.ats_engine import (
    extract_skills,
    calculate_skill_score,
    calculate_keyword_score,
    calculate_ats_score,
    get_matched_skills,
    get_missing_skills
)

from services.analyzer import analyze_resume

from services.course_recommender import (
    recommend_courses
)


def process_candidate(
    job_description,
    resume_text
):
    """
    Complete resume analysis pipeline.
    """

    # -------------------------
    # 1. Extract skills
    # -------------------------

    jd_skills = extract_skills(
        job_description
    )

    resume_skills = extract_skills(
        resume_text
    )

    # -------------------------
    # 2. Calculate skill score
    # -------------------------

    skill_score = calculate_skill_score(
        resume_skills,
        jd_skills
    )

    # -------------------------
    # 3. Calculate keyword score
    # -------------------------

    keyword_score = calculate_keyword_score(
        resume_text,
        job_description
    )

    # -------------------------
    # 4. Calculate ATS score
    # -------------------------

    ats_score = calculate_ats_score(
        skill_score=skill_score,
        keyword_score=keyword_score
    )

    # -------------------------
    # 5. Determine matched skills
    # -------------------------

    matched_skills = get_matched_skills(
        resume_skills,
        jd_skills
    )

    # -------------------------
    # 6. Determine missing skills
    # -------------------------

    missing_skills = get_missing_skills(
        resume_skills,
        jd_skills
    )

    # -------------------------
    # 7. AI analysis
    # -------------------------

    ai_analysis = analyze_resume(
        job_description,
        resume_text
    )

    # -------------------------
    # 8. Course recommendations
    # -------------------------

    courses = recommend_courses(
        missing_skills
    )

    # -------------------------
    # 9. Combine results
    # -------------------------

    return {

        "ats_score": ats_score,

        "skill_score": skill_score,

        "keyword_score": keyword_score,

        "required_skills": jd_skills,

        "resume_skills": resume_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "candidate_name":
            ai_analysis.get(
                "candidate_name",
                ""
            ),

        "summary":
            ai_analysis.get(
                "summary",
                ""
            ),

        "experience_gaps":
            ai_analysis.get(
                "experience_gaps",
                []
            ),

        "education_match":
            ai_analysis.get(
                "education_match",
                ""
            ),

        "strengths":
            ai_analysis.get(
                "strengths",
                []
            ),

        "weaknesses":
            ai_analysis.get(
                "weaknesses",
                []
            ),

        "resume_improvements":
            ai_analysis.get(
                "resume_improvements",
                []
            ),

        "recommended_courses":
            ai_analysis.get(
                "recommended_courses",
                []
            ) + courses
    }

