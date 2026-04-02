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
     "opts": [("Very satisfied",0),("Satisfied",1),("Neutral",2),("Dissatisfied",3),("Very dissatisfied",4)]}
]

psych_states = {
    "Very Low Stress": (0, 15),
    "Low Stress": (16, 30),
    "Moderate Stress": (31, 45),
    "High Stress": (46, 60),
    "Very High Stress": (61, 75),
    "Severe Stress": (76, 90),
    "Critical State": (91, 200)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
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
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": "", "surname": "", "dob": "", "sid": ""}

st.session_state.user_info["name"] = st.text_input("Given Name", st.session_state.user_info["name"])
st.session_state.user_info["surname"] = st.text_input("Surname", st.session_state.user_info["surname"])
st.session_state.user_info["dob"] = st.text_input("Date of Birth (YYYY-MM-DD)", st.session_state.user_info["dob"])
st.session_state.user_info["sid"] = st.text_input("Student ID (digits only)", st.session_state.user_info["sid"])

# --- Initialize session state for survey ---
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# --- Validate user info before starting survey ---
if st.button("Start Survey"):
    errors = []
    info = st.session_state.user_info
    if not validate_name(info["name"]):
        errors.append("Invalid given name.")
    if not validate_name(info["surname"]):
        errors.append("Invalid surname.")
    if not validate_dob(info["dob"]):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not info["sid"].isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

# --- Display current question ---
if st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]
    choice = st.radio(f"Q{st.session_state.current_q+1}. {q['q']}", [opt[0] for opt in q["opts"]])

    if st.button("Next"):
        # Save answer
        score = next(score for label, score in q["opts"] if label == choice)
        st.session_state.answers.append({"question": q["q"], "selected_option": choice, "score": score})
        st.session_state.current_q += 1
        st.experimental_rerun()  # refresh page to show next question

# --- Show results after last question ---
else:
    total_score = sum(a["score"] for a in st.session_state.answers)
    status = interpret_score(total_score)
    st.markdown(f"## ✅ Your Result: {status}")
    st.markdown(f"**Total Score:** {total_score}")

    record = {
        "name": st.session_state.user_info["name"],
        "surname": st.session_state.user_info["surname"],
        "dob": st.session_state.user_info["dob"],
        "student_id": st.session_state.user_info["sid"],
        "total_score": total_score,
        "result": status,
        "answers": st.session_state.answers,
        "version": version_float
    }

    json_filename = f"{st.session_state.user_info['sid']}_result.json"
    save_json(json_filename, record)
    st.success(f"Your results are saved as {json_filename}")
    st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
    {"q": "How often do you feel panic during an exam?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you forget information during tests due to stress?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you practice past exam papers?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How supported do you feel by your teachers in exam preparation?",
     "opts": [("Very supported",0),("Supported",1),("Neutral",2),("Unsupported",3),("Very unsupported",4)]},

    {"q": "How often do you discuss exam material with classmates?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How well do you understand the exam format before the test?",
     "opts": [("Very well",0),("Well",1),("Adequately",2),("Poorly",3),("Very poorly",4)]},

    {"q": "How often do you procrastinate instead of studying?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you feel physically unwell due to exam stress (headaches, nausea)?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How motivated do you feel to study for exams?",
     "opts": [("Very motivated",0),("Motivated",1),("Neutral",2),("Unmotivated",3),("Very unmotivated",4)]},

    {"q": "How often do you use relaxation techniques before exams (breathing, breaks)?",
     "opts": [("Always",0),("Often",1),("Sometimes",2),("Rarely",3),("Never",4)]},

    {"q": "How would you rate your overall level of test anxiety?",
     "opts": [("Very low",0),("Low",1),("Moderate",2),("High",3),("Very high",4)]}
    ]
    
psych_states = {
    "Very Low Stress": (0, 15),
    "Low Stress": (16, 30),
    "Moderate Stress": (31, 45),
    "High Stress": (46, 60),
    "Very High Stress": (61, 75),
    "Severe Stress": (76, 90),
    "Critical State": (91, 200)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
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
st.set_page_config(page_title="Student Psychological Survey")
st.title("📝 Student Psychological Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
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
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
