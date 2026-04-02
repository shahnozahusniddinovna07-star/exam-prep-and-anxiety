import streamlit as st
import json
from datetime import datetime

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "How often do you feel overwhelmed by your responsibilities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How well do you sleep at night?",
     "opts": [("Very well",0),("Fairly well",1),("Occasionally restless",2),("Often restless",3),("Very poorly",4)]},
    {"q": "How often do you feel anxious about exams?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How would you rate your ability to concentrate while studying?",
     "opts": [("Excellent",0),("Good",1),("Fair",2),("Poor",3),("Very poor",4)]},
    {"q": "How often do you procrastinate studying for exams?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How confident do you feel before an exam?",
     "opts": [("Very confident",0),("Confident",1),("Neutral",2),("Unconfident",3),("Very unconfident",4)]},
    {"q": "How often do you review past exam papers?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How well do you manage your study time?",
     "opts": [("Very well",0),("Well",1),("Adequately",2),("Poorly",3),("Very poorly",4)]},
    {"q": "How often do you feel stressed about upcoming exams?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you feel physical symptoms of stress (headache, fatigue)?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "How often do you use relaxation techniques (meditation, breathing)?",
     "opts": [("Daily",0),("Several times a week",1),("Weekly",2),("Rarely",3),("Never",4)]},
    {"q": "How much do distractions affect your studying?",
     "opts": [("Not at all",0),("A little",1),("Somewhat",2),("A lot",3),("Completely",4)]},
    {"q": "How often do you seek help from teachers or peers?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How organized is your study material?",
     "opts": [("Very organized",0),("Organized",1),("Neutral",2),("Disorganized",3),("Very disorganized",4)]},
    {"q": "How often do you set specific goals for your study sessions?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How often do you feel motivated to study?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How well do you balance study with leisure activities?",
     "opts": [("Very well",0),("Well",1),("Fairly well",2),("Poorly",3),("Very poorly",4)]},
    {"q": "How confident are you in recalling studied material during exams?",
     "opts": [("Very confident",0),("Confident",1),("Neutral",2),("Unconfident",3),("Very unconfident",4)]},
    {"q": "How often do you revise immediately after learning new material?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},
    {"q": "How satisfied are you with your exam preparation?",
     "opts": [("Very satisfied",0),("Satisfied",1),("Neutral",2),("Dissatisfied",3),("Very dissatisfied",4)]},
]

psych_states = {
    "Very Low Stress": (0, 15),
    "Low Stress": (16, 30),
    "Moderate Stress": (31, 45),
    "High Stress": (46, 60),
    "Very High Stress": (61, 75),
    "Severe Stress": (76, 90),
    "Critical State": (91, 200),
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except Exception:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Exam Preparation & Test Anxiety Survey")
st.title("📝 Exam Preparation & Test Anxiety Survey")
st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name    = st.text_input("Given Name")
surname = st.text_input("Surname")
dob     = st.text_input("Date of Birth (YYYY-MM-DD)")
sid     = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(s for label, s in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score,
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float,
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button(
            "Download your result JSON",
            json.dumps(record, indent=2),
            file_name=json_filename,
        )
