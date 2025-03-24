from flask import Flask, request, jsonify
import os
import fitz  # PyMuPDF
import spacy
import openai
import PyPDF2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = "your_openai_api_key"  # Replace with your actual OpenAI API key
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_resume_info(text):
    doc = nlp(text)
    skills, education, experience = [], [], []
    
    for ent in doc.ents:
        if ent.label_ == "ORG":
            education.append(ent.text)
        elif ent.label_ == "WORK_OF_ART":
            experience.append(ent.text)
        elif ent.label_ == "PRODUCT":
            skills.append(ent.text)
    
    return {"Skills": list(set(skills)), "Education": list(set(education)), "Experience": list(set(experience))}

def generate_questions(resume_info):
    questions = []
    
    for skill in resume_info["Skills"]:
        questions.append(f"Can you describe how you've applied your knowledge of {skill} in your previous projects?")
    
    for edu in resume_info["Education"]:
        questions.append(f"Can you tell me more about your time at {edu} and how it prepared you for this role?")
    
    for exp in resume_info["Experience"]:
        questions.append(f"Can you explain your role and responsibilities during {exp}? What challenges did you face?")
    
    return questions

@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["resume"]
    pdf_path = os.path.join("uploads", file.filename)
    file.save(pdf_path)
    
    text = extract_text_from_pdf(pdf_path)
    resume_info = extract_resume_info(text)
    questions = generate_questions(resume_info)
    
    return jsonify({"resume_text": text, "resume_info": resume_info, "questions": questions})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
