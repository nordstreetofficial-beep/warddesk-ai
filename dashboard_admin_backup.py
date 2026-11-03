import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(
    page_title="WardDesk AI",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 WardDesk AI")
st.subheader("Hospital Administrative Workflow Assistant")
st.caption("AI-assisted task organisation | Human approval required")

api_key = os.getenv("MODEL_API_KEY")

if not api_key:
    st.error("Meta API key missing. Check your .env file.")
    st.stop()

client = OpenAI(
    base_url="https://api.meta.ai/v1",
    api_key=api_key
)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "suggestion" not in st.session_state:
    st.session_state.suggestion = None

st.info(
    "WardDesk supports administrative workflows only. "
    "It does not diagnose, assess clinical urgency, or approve patient care decisions."
)

st.header("1. Add Hospital Administrative Tasks")

with st.form("task_form"):
    task_name = st.text_input(
        "Task description",
        placeholder="Example: Room cleaning request"
    )

    department = st.selectbox(
        "Responsible department",
        [
            "Housekeeping",
            "Ward Administration",
            "Bed Management",
            "Materials Management",
            "Procurement",
            "Other"
        ]
    )

    deadline = st.selectbox(
        "Deadline",
        [
            "Within 15 minutes",
            "Within 30 minutes",
            "Within 1 hour",
            "Within 4 hours",
            "By end of today",
            "Tomorrow",
            "No fixed deadline"
        ]
    )

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task_name.strip():
            st.session_state.tasks.append({
                "task": task_name.strip(),
                "department": department,
                "deadline": deadline,
                "status": "Pending"
            })
            st.session_state.suggestion = None
            st.success("Task added successfully.")
        else:
            st.warning("Please enter a task description.")

st.divider()

st.header("2. Current Task List")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        st.write(
            f"**{i + 1}. {task['task']}** — "
            f"{task['department']} — "
            f"{task['deadline']} — "
            f"Status: {task['status']}"
        )

    if st.button("🤖 Ask Muse Spark to Prioritise Tasks"):
        task_text = "\n".join(
            [
                f"Task {i + 1}: {t['task']}; "
                f"Department: {t['department']}; "
                f"Deadline: {t['deadline']}"
                for i, t in enumerate(st.session_state.tasks)
            ]
        )

        prompt = f"""
You are WardDesk, a hospital administrative workflow assistant.

Prioritise these fictional administrative tasks:

{task_text}

Return:
1. Priority ranking.
2. Reason for each ranking.
3. Responsible department.
4. Suggested next action.
5. What requires human approval.

Rules:
- Use only the information supplied.
- Do not diagnose or assess clinical urgency.
- Do not approve discharge, admission or patient care.
- Flag missing information instead of inventing facts.
- All recommendations require human review.
"""

        try:
            with st.spinner("Muse Spark is analysing administrative tasks..."):
                response = client.responses.create(
                    model="muse-spark-1.3",
                    input=prompt
                )

            st.session_state.suggestion = response.output_text

        except Exception as e:
            st.error(f"Meta API error: {e}")

else:
    st.info("No tasks added yet. Add your first task above.")

st.divider()

st.header("3. AI Prioritisation Recommendation")

if st.session_state.suggestion:
    st.markdown(st.session_state.suggestion)

    st.warning("Human approval required before acting on recommendations.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve Recommendation"):
            for task in st.session_state.tasks:
                if task["status"] == "Pending":
                    task["status"] = "Approved"
            st.session_state.suggestion = None
            st.success("Recommendation approved by demo user.")
            st.rerun()

    with col2:
        if st.button("❌ Reject Recommendation"):
            st.session_state.suggestion = None
            st.warning("Recommendation rejected. Tasks remain pending.")
            st.rerun()

st.divider()

st.header("4. Task History")

if st.session_state.tasks:
    for task in st.session_state.tasks:
        st.write(
            f"{task['task']} | "
            f"{task['department']} | "
            f"{task['status']}"
        )
else:
    st.write("No task history yet.")

st.caption(
    "WardDesk Hackathon Prototype | Synthetic data only | "
    "Not for clinical decision-making"
)