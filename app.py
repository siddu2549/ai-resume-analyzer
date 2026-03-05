from flask import Flask, render_template, request, jsonify
import os

from database import init_db, save_resume, get_all_resumes
from analyzer.parser import extract_text
from analyzer.skill_extractor import extract_skills
from analyzer.scorer import score_resume

app = Flask(__name__)

# Initialize database
init_db()

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Check if file exists
    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        # Extract resume text
        text = extract_text(filepath)

        # Detect skills
        skills = extract_skills(text)

        # Calculate score
        score = score_resume(text, skills)

        # Save to database
        save_resume(file.filename, score, skills)

        # Prepare result JSON
        result = {
            "overall_score": score,
            "ats_score": max(score - 5, 0),
            "impact_score": max(score - 10, 0),

            "skills": {
                "tech": skills,
                "soft": ["communication", "teamwork"],
                "tools": ["git", "vscode"]
            },

            "improvements": [
                {"text": "Add measurable achievements in your projects"},
                {"text": "Include more industry keywords related to your field"},
                {"text": "Add a professional summary at the top of the resume"}
            ]
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ⭐ NEW ROUTE FOR HISTORY PAGE
@app.route("/history")
def history():

    resumes = get_all_resumes()

    return render_template(
        "history.html",
        resumes=resumes
    )
@app.route("/analytics")
def analytics():

    resumes = get_all_resumes()

    total_resumes = len(resumes)

    # Average score
    if total_resumes > 0:
        avg_score = sum(r[1] for r in resumes) / total_resumes
    else:
        avg_score = 0

    # -------- Skill Analytics --------
    skill_count = {}

    for r in resumes:

        skills = r[2].split(",")

        for skill in skills:

            skill = skill.strip().lower()

            if skill in skill_count:
                skill_count[skill] += 1
            else:
                skill_count[skill] = 1

    # Convert dictionary to lists
    skill_names = list(skill_count.keys())
    skill_values = list(skill_count.values())

    return render_template(
        "analytics.html",
        total=total_resumes,
        average_score=round(avg_score,2),
        resumes=resumes,
        skill_names=skill_names,
        skill_values=skill_values
    )

if __name__ == "__main__":
    app.run(debug=True)