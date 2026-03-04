skills_database = [
    "python",
    "java",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",
    "data analysis",
    "flask",
    "django",
    "react",
    "node.js"
]

def extract_skills(text):

    text = text.lower()

    detected_skills = []

    for skill in skills_database:
        if skill in text:
            detected_skills.append(skill)

    return detected_skills