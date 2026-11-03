import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ==========================================
# 1. CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("MODEL_API_KEY")
MODEL_NAME = "muse-spark-1.3"

st.set_page_config(
    page_title="WardDesk AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# 2. SESSION STATE
# ==========================================

if "incidents" not in st.session_state:
    st.session_state.incidents = []


# ==========================================
# 3. CUSTOM STYLING
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        min-height: 42px;
    }

    div[data-testid="stForm"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
    }

    .small-note {
        color: #64748B;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. LANDING HEADER
# ==========================================

with st.container(border=True):

    st.caption("HOSPITAL IT OPERATIONS PLATFORM")

    st.title("🏥 WardDesk AI")

    st.subheader(
        "AI First-Responder for Hospital IT Support"
    )

    st.markdown(
        "**Powered by Meta Muse Spark**  |  "
        "Human-supervised workflow  |  "
        "Synthetic demonstration environment"
    )
# ==========================================
# 5. META MUSE SPARK CONNECTION
# ==========================================

def get_ai_client():
    if not API_KEY:
        return None

    return OpenAI(
        api_key=API_KEY,
        base_url="https://api.meta.ai/v1"
    )


# ==========================================
# 6. STATIC RUNBOOK GUIDANCE
# ==========================================

RUNBOOKS = {
    "HIS Application": [
        "Confirm whether the issue affects one user or multiple users.",
        "Record the affected application and error message.",
        "Check whether the workstation has network connectivity.",
        "Escalate application-level errors to the authorised application support team."
    ],
    "Network": [
        "Identify the affected workstation, ward or department.",
        "Check network cable and connection indicators.",
        "Check whether other users in the same area are affected.",
        "Escalate suspected network infrastructure faults to the network team."
    ],
    "Printer": [
        "Check printer power and connection status.",
        "Confirm paper and toner availability.",
        "Check for displayed error messages or paper jams.",
        "Escalate persistent hardware faults to the authorised support team."
    ],
    "User Account": [
        "Confirm the user's identity through the organisation's approved process.",
        "Record the exact login error.",
        "Check whether the account may be locked or expired.",
        "Escalate account permission issues to the authorised administrator."
    ],
    "Workstation": [
        "Record the workstation asset number or location.",
        "Check power, display and peripheral connections.",
        "Record any error messages.",
        "Escalate suspected hardware faults to the desktop support team."
    ],
    "Other": [
        "Record the reported symptoms and affected location.",
        "Establish whether the issue affects one or multiple users.",
        "Collect relevant error messages.",
        "Escalate to the appropriate IT support team."
    ]
}


# ==========================================
# 7. SIMULATED DIAGNOSTICS
# ==========================================

def run_simulated_diagnostics(system):
    results = {
        "HIS Application": [
            "Synthetic check: application availability requires technician verification.",
            "Synthetic check: user impact information should be confirmed.",
            "No live hospital system was accessed."
        ],
        "Network": [
            "Synthetic check: network connectivity requires technician verification.",
            "Synthetic check: affected network area should be confirmed.",
            "No live network devices were accessed."
        ],
        "Printer": [
            "Synthetic check: printer power and connectivity require verification.",
            "Synthetic check: paper and toner status require verification.",
            "No physical printer was accessed."
        ],
        "User Account": [
            "Synthetic check: account status requires authorised administrator verification.",
            "Synthetic check: access permissions were not changed.",
            "No user account was accessed."
        ],
        "Workstation": [
            "Synthetic check: workstation power and hardware require verification.",
            "Synthetic check: asset information should be confirmed.",
            "No workstation was accessed."
        ],
        "Other": [
            "Synthetic check: issue details require technician assessment.",
            "Synthetic check: affected services should be confirmed.",
            "No production system was accessed."
        ]
    }

    return results.get(system, results["Other"])


# ==========================================
# 8. DASHBOARD METRICS
# ==========================================

incidents = st.session_state.incidents

total_incidents = len(incidents)
awaiting = sum(
    1 for item in incidents
    if item["status"] == "Awaiting Decision"
)
approved = sum(
    1 for item in incidents
    if item["status"] == "Approved"
)
rejected = sum(
    1 for item in incidents
    if item["status"] == "Rejected"
)

st.subheader("📊 Incident Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", total_incidents)
col2.metric("Awaiting Decision", awaiting)
col3.metric("Approved", approved)
col4.metric("Rejected", rejected)

st.divider()


# ==========================================
# 9. NEW INCIDENT FORM
# ==========================================

st.subheader("📝 Report a New IT Incident")

with st.form("incident_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        reporter = st.text_input(
            "Reporter / Department",
            placeholder="Example: Emergency Department"
        )

        system = st.selectbox(
            "Affected IT System",
            [
                "HIS Application",
                "Network",
                "Printer",
                "User Account",
                "Workstation",
                "Other"
            ]
        )

    with col2:
        location = st.text_input(
            "Location",
            placeholder="Example: Ward 3"
        )

        urgency = st.selectbox(
            "Reported Urgency",
            [
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

    description = st.text_area(
        "Incident Description",
        placeholder="Describe the IT problem, error message and number of affected users...",
        height=120
    )

    submitted = st.form_submit_button(
        "➕ Submit Incident",
        use_container_width=True
    )

    if submitted:
        if not description.strip():
            st.error("Please enter an incident description.")

        else:
            incident = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "reporter": reporter.strip() or "Not provided",
                "system": system,
                "location": location.strip() or "Not provided",
                "urgency": urgency,
                "description": description.strip(),
                "created": datetime.now().strftime("%d %b %Y, %H:%M:%S"),
                "status": "Awaiting Decision",
                "ai_analysis": None,
                "diagnostics": None
            }

            st.session_state.incidents.insert(0, incident)

            st.success("Incident successfully submitted.")

            st.rerun()


# ==========================================
# 10. INCIDENT MANAGEMENT
# ==========================================

st.divider()
st.subheader("🖥️ Incident Management")

if not st.session_state.incidents:

    st.info("No incidents have been submitted yet. Use the form above to create a demonstration incident.")

else:

    for incident in st.session_state.incidents:

        with st.container(border=True):

            st.markdown(
                f"### 🎫 Incident #{incident['id'][-6:]}"
            )

            col1, col2, col3 = st.columns(3)

            col1.write(f"**System:** {incident['system']}")
            col2.write(f"**Urgency:** {incident['urgency']}")
            col3.write(f"**Status:** {incident['status']}")

            st.write(f"**Reporter:** {incident['reporter']}")
            st.write(f"**Location:** {incident['location']}")
            st.write(f"**Reported:** {incident['created']}")
            st.write(f"**Description:** {incident['description']}")

            # ----------------------------------
            # RUNBOOK GUIDANCE
            # ----------------------------------

            with st.expander("📘 Troubleshooting Runbook Guidance"):

                for step_number, step in enumerate(
                    RUNBOOKS[incident["system"]], start=1
                ):
                    st.write(f"{step_number}. {step}")

                st.caption(
                    "Static demonstration guidance. Verify procedures against "
                    "your organisation's approved runbooks."
                )

            # ----------------------------------
            # AI ANALYSIS
            # ----------------------------------

            st.markdown("#### 🤖 AI Prioritisation Recommendation")

            if st.button(
                "✨ Analyse with Meta Muse Spark",
                key=f"analyse_{incident['id']}",
                use_container_width=True
            ):

                client = get_ai_client()

                if client is None:
                    st.error(
                        "Meta API key not found. Check that MODEL_API_KEY "
                        "is configured in your local .env file."
                    )

                else:

                    prompt = f"""
You are WardDesk AI, an assistant for hospital IT support teams.

Analyse the following fictional hospital IT incident.

This is administrative IT support assistance only.
Do not provide clinical advice or make patient-care decisions.
Do not claim that you accessed real hospital systems.
Do not invent diagnostic results.

INCIDENT INFORMATION

Affected system: {incident['system']}
Reported urgency: {incident['urgency']}
Department or reporter: {incident['reporter']}
Location: {incident['location']}
Description: {incident['description']}

Provide the response using these sections:

1. Suggested IT Priority
Choose Critical, High, Medium or Low.
Explain that this is a recommendation for human review.

2. Reason for Recommendation
Explain the operational factors in the supplied description.
Do not invent facts.

3. Recommended First Response
Give practical, non-destructive IT troubleshooting steps.

4. Suggested Escalation Team
Recommend an appropriate IT support team based on the supplied system.

5. Information Still Required
List any missing information that a technician should collect.

6. Human Review
State that an authorised IT technician must verify the recommendation
before taking consequential action.

Do not independently approve, reject, close or modify the incident.
"""

                    try:

                        with st.spinner(
                            "Meta Muse Spark is analysing the incident..."
                        ):

                            response = client.responses.create(
                                model=MODEL_NAME,
                                input=prompt
                            )

                        incident["ai_analysis"] = response.output_text

                        st.success("AI analysis completed.")

                    except Exception as error:

                        st.error(
                            f"AI analysis could not be completed: {error}"
                        )

            if incident["ai_analysis"]:

                with st.expander(
                    "View AI Analysis",
                    expanded=True
                ):

                    st.markdown(incident["ai_analysis"])

            # ----------------------------------
            # SIMULATED DIAGNOSTICS
            # ----------------------------------

            st.markdown("#### 🔍 Demonstration Diagnostics")

            if st.button(
                "Run Simulated Diagnostics",
                key=f"diagnostics_{incident['id']}"
            ):

                incident["diagnostics"] = run_simulated_diagnostics(
                    incident["system"]
                )

            if incident["diagnostics"]:

                for result in incident["diagnostics"]:
                    st.write(f"• {result}")

                st.caption(
                    "These are simulated demonstration messages, not results "
                    "from live hospital infrastructure."
                )

            # ----------------------------------
            # HUMAN APPROVAL
            # ----------------------------------

            st.markdown("#### 👤 Human Review and Decision")

            if incident["status"] == "Awaiting Decision":

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Approve for IT Follow-up",
                        key=f"approve_{incident['id']}",
                        use_container_width=True
                    ):

                        incident["status"] = "Approved"
                        st.rerun()

                with col2:

                    if st.button(
                        "❌ Reject Recommendation",
                        key=f"reject_{incident['id']}",
                        use_container_width=True
                    ):

                        incident["status"] = "Rejected"
                        st.rerun()

            else:

                st.info(
                    f"Human review status: {incident['status']}"
                )

            # ----------------------------------
            # ESCALATION TICKET DOWNLOAD
            # ----------------------------------

            ticket_text = f"""
WARDDESK AI - IT INCIDENT ESCALATION NOTE

Incident ID: {incident['id']}
Reported: {incident['created']}

Reporter / Department: {incident['reporter']}
Location: {incident['location']}
Affected System: {incident['system']}
Reported Urgency: {incident['urgency']}

Incident Description:
{incident['description']}

AI Analysis:
{incident['ai_analysis'] or 'AI analysis has not been generated.'}

Human Review Status:
{incident['status']}

IMPORTANT:
This is a demonstration escalation note.
AI recommendations require review by an authorised IT technician.
No live hospital infrastructure was accessed.
"""

            st.download_button(
                label="📥 Download Escalation Ticket",
                data=ticket_text,
                file_name=f"WardDesk_Incident_{incident['id']}.txt",
                mime="text/plain",
                key=f"download_{incident['id']}"
            )


# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption("WardDesk AI | AI First-Responder for Hospital IT Support")

st.markdown(
    "**Meta Global AI Developer Hackathon 2026**  \n"
    "Demonstration prototype | Synthetic scenarios | "
    "Human-supervised workflow"
)