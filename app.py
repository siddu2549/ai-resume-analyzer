from flask import Flask, render_template, request, jsonify
import os

from analyzer.parser import extract_text
from analyzer.skill_extractor import extract_skills
from analyzer.scorer import score_resume

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)