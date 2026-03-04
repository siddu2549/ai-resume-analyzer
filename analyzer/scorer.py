def score_resume(text, skills):

    score = 0

    # Skill score
    score += len(skills) * 5

    # Check sections
    text = text.lower()

    if "project" in text:
        score += 10

    if "experience" in text:
        score += 10

    if "education" in text:
        score += 5

    # Limit score to 100
    if score > 100:
        score = 100

    return score