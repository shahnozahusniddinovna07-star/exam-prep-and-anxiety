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
    "Very Low Stress":  (0,  15),
    "Low Stress":       (16, 30),
    "Moderate Stress":  (31, 45),
    "High Stress":      (46, 60),
    "Very High Stress": (61, 75),
    "Severe Stress":    (76, 90),
    "Critical State":   (91, 200),
}

descriptions = {
    "Very Low Stress":  "Stable mental state. Excellent preparation habits. No help needed.",
    "Low Stress":       "Mild tension. Good preparation. Self-care is recommended.",
    "Moderate Stress":  "Noticeable anxiety. Consider improving study strategies.",
    "High Stress":      "Elevated anxiety. Advisable to seek academic or psychological support.",
    "Very High Stress": "Significant distress. Professional help is recommended.",
    "Severe Stress":    "Urgent psychological intervention needed.",
    "Critical State":   "Immediate medical or psychological assistance required.",
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    import re
    return bool(re.match(r"^[a-zA-Z][a-zA-Z\-' ]*$", name.strip()))

def validate_dob(dob: str) -> bool:
    try:
        dt = datetime.strptime(dob.strip(), "%Y-%m-%d")
        return dt < datetime.now()
    except Exception:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

# ---------------- SESSION STATE INIT ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "info"
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "answers_list" not in st.session_state:
    st.session_state.answers_list = []
if "total_score" not in st.session_state:
    st.session_state.total_score = 0

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Exam Preparation & Test Anxiety Survey")
st.title("📝 Exam Preparation & Test Anxiety Survey")

# ════════════════════════════════════════════
# STAGE 1 — User Info
# ════════════════════════════════════════════
if st.session_state.stage == "info":
    st.info("Please fill out your details below, then click **Start Survey**.")

    name    = st.text_input("Given Name",                 value=st.session_state.user_info.get("name", ""))
    surname = st.text_input("Surname",                    value=st.session_state.user_info.get("surname", ""))
    dob     = st.text_input("Date of Birth (YYYY-MM-DD)", value=st.session_state.user_info.get("dob", ""))
    sid     = st.text_input("Student ID (digits only)",   value=st.session_state.user_info.get("sid", ""))

    if st.button("Start Survey"):
        errors = []
        if not validate_name(name):
            errors.append("Invalid given name — only letters, hyphens, apostrophes and spaces allowed.")
        if not validate_name(surname):
            errors.append("Invalid surname — only letters, hyphens, apostrophes and spaces allowed.")
        if not validate_dob(dob):
            errors.append("Invalid date of birth. Use YYYY-MM-DD format with a past date.")
        if not sid.strip().isdigit():
            errors.append("Student ID must contain digits only.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.session_state.user_info = {
                "name":    name.strip(),
                "surname": surname.strip(),
                "dob":     dob.strip(),
                "sid":     sid.strip(),
            }
            st.session_state.stage = "survey"
            st.rerun()

# ════════════════════════════════════════════
# STAGE 2 — Survey (all questions in one form)
# ════════════════════════════════════════════
elif st.session_state.stage == "survey":
    info = st.session_state.user_info
    st.success(f"Welcome, {info['name']} {info['surname']}! Answer all {len(questions)} questions and click Submit.")
    st.markdown("---")

    with st.form("survey_form"):
        form_answers = {}
        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.radio(
                f"**Q{idx+1}.** {q['q']}",
                opt_labels,
                key=f"q_{idx}",
                index=0,
            )
            form_answers[idx] = choice

        submitted = st.form_submit_button("✅ Submit Survey")

    if submitted:
        answers_list = []
        total_score  = 0
        for idx, q in enumerate(questions):
            chosen_label = form_answers[idx]
            score = next(s for label, s in q["opts"] if label == chosen_label)
            total_score += score
            answers_list.append({
                "question":        q["q"],
                "selected_option": chosen_label,
                "score":           score,
            })
        st.session_state.answers_list = answers_list
        st.session_state.total_score  = total_score
        st.session_state.stage        = "results"
        st.rerun()

# ════════════════════════════════════════════
# STAGE 3 — Results
# ════════════════════════════════════════════
elif st.session_state.stage == "results":
    info        = st.session_state.user_info
    total_score = st.session_state.total_score
    answers     = st.session_state.answers_list
    status      = interpret_score(total_score)

    st.balloons()
    st.markdown(f"## ✅ Result for {info['name']} {info['surname']}")
    st.markdown(f"**Total Score:** {total_score} / {len(questions) * 4}")
    st.markdown(f"**Psychological State:** `{status}`")
    st.info(descriptions.get(status, ""))
    st.markdown("---")

    record = {
        "name":        info["name"],
        "surname":     info["surname"],
        "dob":         info["dob"],
        "student_id":  info["sid"],
        "total_score": total_score,
        "max_score":   len(questions) * 4,
        "result":      status,
        "answers":     answers,
        "version":     version_float,
        "date_taken":  datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    st.download_button(
        label="⬇️ Download your result (JSON)",
        data=json.dumps(record, indent=2),
        file_name=f"{info['sid']}_result.json",
        mime="application/json",
    )

    with st.expander("📋 View detailed answers"):
        for i, a in enumerate(answers, 1):
            st.markdown(f"**Q{i}.** {a['question']}")
            st.markdown(f"→ {a['selected_option']} *(score: {a['score']})*")

    st.markdown("---")
    if st.button("🔄 Start a new survey"):
        for key in ["stage", "user_info", "answers_list", "total_score"]:
            st.session_state.pop(key, None)
        st.rerun()
