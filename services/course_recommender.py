#!/usr/bin/env python
# coding: utf-8

# In[ ]:


COURSE_MAP = {

    "python": [
        "Python Programming Fundamentals",
        "Advanced Python Development"
    ],

    "sql": [
        "SQL Fundamentals",
        "Advanced SQL and Database Design"
    ],

    "machine learning": [
        "Machine Learning Fundamentals",
        "Applied Machine Learning with Python"
    ],

    "deep learning": [
        "Deep Learning Fundamentals",
        "Neural Networks with PyTorch"
    ],

    "aws": [
        "AWS Cloud Fundamentals",
        "AWS Solutions Architecture Fundamentals"
    ],

    "docker": [
        "Docker Fundamentals",
        "Containerization with Docker"
    ],

    "kubernetes": [
        "Kubernetes Fundamentals",
        "Container Orchestration with Kubernetes"
    ],

    "flask": [
        "Flask Web Development",
        "Building REST APIs with Flask"
    ],

    "django": [
        "Django Web Development",
        "Building Web Applications with Django"
    ],

    "react": [
        "React Fundamentals",
        "Modern React Development"
    ],

    "javascript": [
        "JavaScript Fundamentals",
        "Modern JavaScript Development"
    ],

    "sql": [
        "SQL Fundamentals",
        "Advanced SQL"
    ],

    "git": [
        "Git and GitHub Fundamentals",
        "Advanced Git Workflows"
    ],

    "pandas": [
        "Pandas for Data Analysis",
        "Data Analysis with Python"
    ],

    "tensorflow": [
        "TensorFlow Fundamentals",
        "Deep Learning with TensorFlow"
    ],

    "pytorch": [
        "PyTorch Fundamentals",
        "Deep Learning with PyTorch"
    ]
}


def recommend_courses(missing_skills):
    """Return learning recommendations for missing skills."""

    recommendations = []

    for skill in missing_skills:

        skill_lower = skill.lower()

        if skill_lower in COURSE_MAP:

            recommendations.extend(
                COURSE_MAP[skill_lower]
            )

        else:

            recommendations.append(
                f"Learn {skill.title()} fundamentals"
            )

    # Remove duplicates
    recommendations = list(
        dict.fromkeys(recommendations)
    )

    return recommendations[:10]

