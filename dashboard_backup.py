import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# ==========================================
# WARDDESK AI - COMPLETE HACKATHON MVP
# ==========================================

load_dotenv()

API_KEY = os.getenv("MODEL_API_KEY")
MODEL_NAME = "muse-spark-1.3"

st.set_page_config(
    page_title="WardDesk AI",
    page_icon="🏥",
    layout="wide"
)

# Initialise incident history
if "incidents" not in st.session_state:
    st.session_state.incidents = []

# Professional WardDesk landing header
st.markdown("""
<div style="
    background: linear-gradient(120deg, #102A43, #164E63);
    padding: 30px;
    border-radius: 16px;
    color: white;
    margin-bottom: 22px;
">
    <div style="font-size: 14px; color: #99F6E4;
                font-weight: 600; letter-spacing: 1px;">
        HOSPITAL IT OPERATIONS PLATFORM
    </div>
    <div style="font-size: 34px; font-weight: 750;
                margin-top: 8px;">
        🏥 WardDesk AI
    </div>
    <div style="font-size: 18px; margin-top: 8px;">
        AI First-Responder for Hospital IT Support
    </div>
    <div style="font-size: 13px; color: #DCE7F0;
                margin-top: 16px;">
        Powered by Meta Muse Spark | Human-supervised workflow |
        Synthetic demonstration environment
    </div>
</div>
""", unsafe_allow_html=True)

st.info(
    "WardDesk supports hospital IT personnel with incident "
    "analysis and operational recommendations. It does not "
    "diagnose patients, make clinical decisions or access "
    "hospital production systems."
)
if API_KEY:
    st.success("Meta Muse Spark connection configured")
else:
    st.error(
        "Meta API key not found. Check MODEL_API_KEY in your .env file."
    )
st.markdown("""
<style>

/* Main application background */
.stApp {
    background: #F4F7FB;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Primary action buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    min-height: 44px;
    font-weight: 600;
    border: 1px solid #D5DFEA;
    background: #FFFFFF;
    color: #183153;
    transition: all 0.2s ease;
}

/* Hover effect */
.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #2563EB;
    color: #1D4ED8;
    background: #EFF6FF;
}

/* Download button */
.stDownloadButton > button {
    background: #0F766E;
    color: white;
    border: none;
}

.stDownloadButton > button:hover {
    background: #115E59;
    color: white;
}

/* Section headings */
h1, h2, h3 {
    color: #183153;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

/* Form */
div[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 20px;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

/* Success and info messages */
div[data-testid="stAlert"] {
    border-radius: 9px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# META API CLIENT
# ==========================================

client = None

if API_KEY:
    client = OpenAI(
        base_url="https://api.meta.ai/v1",
        api_key=API_KEY
    )

# ==========================================
# TROUBLESHOOTING RUNBOOKS
# ==========================================

RUNBOOKS = {
    "HIS Application": {
        "title": "HIS Application Troubleshooting",
        "steps": [
            "Record the affected HIS application and error message.",
            "Confirm whether the issue affects one or multiple users.",
            "Check workstation network connectivity using approved tools.",
            "Check HIS service status through authorised monitoring.",
            "Escalate to the HIS application support team if unresolved."
        ]
    },
    "Network": {
        "title": "Network Troubleshooting",
        "steps": [
            "Identify affected users and network locations.",
            "Check physical network connections using approved procedures.",
            "Review authorised network monitoring information.",
            "Check whether other network services are affected.",
            "Escalate unresolved issues to the network team."
        ]
    },
    "Printer": {
        "title": "Printer Troubleshooting",
        "steps": [
            "Record printer name and location.",
            "Check printer power and connection.",
            "Review printer status and pending queue.",
            "Check workstation printer configuration.",
            "Escalate unresolved issues to IT support."
        ]
    },
    "User Account": {
        "title": "User Account Troubleshooting",
        "steps": [
            "Confirm the affected user account.",
            "Record the authentication error.",
            "Check account status using authorised tools.",
            "Follow approved account recovery procedures.",
            "Escalate unresolved access issues."
        ]
    },
    "Workstation": {
        "title": "Workstation Troubleshooting",
        "steps": [
            "Record workstation asset details.",
            "Confirm the reported problem.",
            "Check power and network connectivity.",
            "Review authorised endpoint monitoring.",
            "Escalate unresolved hardware or software issues."
        ]
    },
    "Other": {
        "title": "General IT Troubleshooting",
        "steps": [
            "Record the incident description.",
            "Identify affected users and equipment.",
            "Collect relevant error messages.",
            "Perform approved initial checks.",
            "Escalate to the relevant IT support team."
        ]
    }
}

# ==========================================
# SIMULATED DIAGNOSTICS
# ==========================================

def run_simulated_diagnostics(system):

    results = {
        "HIS Application": [
            "Simulated HIS endpoint: UNAVAILABLE",
            "Simulated network connectivity: PASSED",
            "Simulated service status: REQUIRES REVIEW"
        ],
        "Network": [
            "Simulated gateway status: FAILED",
            "Simulated connectivity: FAILED",
            "Simulated network review: REQUIRED"
        ],
        "Printer": [
            "Simulated printer status: OFFLINE",
            "Simulated print queue: PENDING",
            "Simulated printer review: REQUIRED"
        ],
        "User Account": [
            "Simulated account status: LOCKED",
            "Simulated authentication: FAILED",
            "Simulated account review: REQUIRED"
        ],
        "Workstation": [
            "Simulated endpoint check: COMPLETED",
            "Simulated workstation status: REQUIRES REVIEW",
            "Simulated investigation: REQUIRED"
        ],
        "Other": [
            "No predefined diagnostic profile available.",
            "Manual IT investigation required."
        ]
    }

    return results.get(system, results["Other"])


# ==========================================
# SESSION STATE
# ==========================================

# Dashboard metric styling

st.markdown("""

<style>
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}
div[data-testid="stMetricLabel"] {
    color: #475569;
    font-weight: 600;
}
div[data-testid="stMetricValue"] {
    color: #12304A;
    font-weight: 750;
}
</style>""", unsafe_allow_html=True)

# Dashboard summary

incidents = st.session_state.incidents

total_incidents = len(incidents)

awaiting_review = sum(
1 for item in incidents
if item["status"] not in ["Approved", "Rejected"]
)

approved_count = sum(
1 for item in incidents
if item["status"] == "Approved"
)

rejected_count = sum(
1 for item in incidents
if item["status"] == "Rejected"
)

st.markdown("### Incident Overview")

card1, card2, card3, card4 = st.columns(4)

with card1:
    st.metric("Total Incidents", total_incidents)

with card2:
    st.metric("Awaiting Decision", awaiting_review)

with card3:
    st.metric("Approved", approved_count)

with card4:
    st.metric("Rejected", rejected_count)

st.divider()
else:

    for incident in st.session_state.incidents:

        with st.expander(
            f"Incident #{incident['id']} — "
            f"{incident['system']} — {incident['status']}",
            expanded=True
        ):

            st.write("**Description:**", incident["description"])
            st.write("**System:**", incident["system"])
            st.write("**Department:**", incident["department"])
            st.write("**Operational impact:**", incident["impact"])
            st.write("**Workaround:**", incident["workaround"])
            st.write("**Response target:**", incident["deadline"])

            # ==================================
            # 3. TROUBLESHOOTING RUNBOOK
            # ==================================

            st.header("3. Relevant Troubleshooting Runbook")

            runbook = RUNBOOKS[incident["system"]]

            st.markdown(f"**{runbook['title']}**")

            for step in runbook["steps"]:
                st.write(f"• {step}")

            # ==================================
            # 4. AI INCIDENT ANALYSIS
            # ==================================

            st.header("4. AI Incident Analysis")

            if st.button(
                "🧠  Analyse with Muse Spark",
                key=f"analyse_{incident['id']}"
            ):

                if not client:
                    st.error("Meta API is not configured.")

                else:

                    prompt = f"""
You are WardDesk, an AI first-responder
for hospital IT support personnel.

Analyse this fictional IT incident using
ONLY the information supplied.

INCIDENT:
{incident['description']}

AFFECTED SYSTEM:
{incident['system']}

DEPARTMENT:
{incident['department']}

IMPACT:
{incident['impact']}

WORKAROUND:
{incident['workaround']}

RESPONSE TARGET:
{incident['deadline']}

AVAILABLE TROUBLESHOOTING RUNBOOK:
{runbook['title']}

{chr(10).join(runbook['steps'])}

Provide:

1. Incident category.
2. Suggested operational priority P1-P4.
3. Reason for the suggested priority.
4. Relevant troubleshooting steps from the supplied runbook.
5. Information still required.
6. Recommended human IT action.
7. Whether escalation is recommended.

IMPORTANT RULES:

- Use only the supplied information.
- Do not invent diagnostic results.
- Do not make clinical decisions.
- Do not diagnose patients.
- Do not execute commands.
- Do not modify any systems.
- Require human IT review.
- P1-P4 are suggestions, not validated hospital SLAs.
- Distinguish known information from unknown information.
"""

                    try:

                        with st.spinner(
                            "Muse Spark is analysing the incident..."
                        ):

                            response = client.responses.create(
                                model=MODEL_NAME,
                                input=prompt
                            )

                            incident["analysis"] = response.output_text

                        st.success("Muse Spark analysis completed.")

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Muse Spark API error: {error}"
                        )

            if incident["analysis"]:

                st.markdown("### AI Recommendation")
                st.write(incident["analysis"])

            # ==================================
            # 5. SIMULATED DIAGNOSTICS
            # ==================================

            st.header("5. Simulated Diagnostics")

            st.caption(
                "These are predetermined synthetic results. "
                "No real hospital systems are accessed."
            )

            if st.button(
                "🔍  Run Simulated Diagnostics",
                key=f"diagnostics_{incident['id']}"
            ):

                incident["diagnostics"] = (
                    run_simulated_diagnostics(
                        incident["system"]
                    )
                )

                st.rerun()

            if incident["diagnostics"]:

                for result in incident["diagnostics"]:
                    st.write(f"• {result}")

           # ==================================
            # 6. HUMAN APPROVAL
            # ==================================

            st.header("6. Human Approval")

            if not incident["analysis"]:

                st.info("Waiting for Muse Spark analysis.")

            elif not incident["diagnostics"]:

                st.warning(
                    "Please complete simulated diagnostics "
                    "before reviewing the recommendation."
                )

            else:

                st.success(
                    "AI analysis and simulated diagnostics completed. "
                    "Human review is now available."
                )

                if incident["status"] in ["Approved", "Rejected"]:
                    st.info(
                        f"Recorded human decision: {incident['status']}"
                    )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "✅ Approve Recommendation",
                        key=f"approve_{incident['id']}",
                        use_container_width=True,
                        disabled=incident["status"] in ["Approved", "Rejected"]
                    ):

                        incident["status"] = "Approved"
                        st.rerun()

                with col2:

                    if st.button(
                        "❌ Reject Recommendation",
                        key=f"reject_{incident['id']}",
                        use_container_width=True,
                        disabled=incident["status"] in ["Approved", "Rejected"]
                    ):

                        incident["status"] = "Rejected"
                        st.rerun()
            # ==================================
            # 7. ESCALATION TICKET
            # ==================================

            st.header("7. Escalation Ticket")

            if incident["status"] not in ["Approved", "Rejected"]:

                st.warning(
                    "A human approval or rejection is required "
                    "before generating the ticket."
                )

            elif not incident["analysis"] or not incident["diagnostics"]:

                st.warning(
                    "Complete AI analysis and diagnostics first."
                )

            else:

                diagnostic_text = "\n".join(
                    f"- {item}"
                    for item in incident["diagnostics"]
                )

                ticket_text = f"""
WARDDESK AI - IT INCIDENT ESCALATION TICKET
============================================

Incident ID: {incident['id']}
Reported at: {incident['reported_at']}
System: {incident['system']}
Department: {incident['department']}
Incident Status: {incident['status']}

INCIDENT DESCRIPTION
--------------------
{incident['description']}

OPERATIONAL IMPACT
------------------
{incident['impact']}

WORKAROUND AVAILABLE
--------------------
{incident['workaround']}

RESPONSE TARGET
---------------
{incident['deadline']}

AI INCIDENT ANALYSIS
--------------------
{incident['analysis']}

SIMULATED DIAGNOSTICS
---------------------
{diagnostic_text}

HUMAN DECISION
--------------
{incident['status']}

IMPORTANT NOTICE
----------------
This ticket uses synthetic demonstration data.
Diagnostics are simulated.
No real hospital systems were accessed.
Human IT personnel must verify all recommendations.

Generated by WardDesk AI
Powered by Meta Muse Spark
"""

                st.download_button(
                    label="📄  Download Escalation Ticket",
                    data=ticket_text,
                    file_name=(
                        f"WardDesk_Incident_{incident['id']}.txt"
                    ),
                    mime="text/plain",
                    key=f"download_ticket_{incident['id']}"
                )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "WardDesk AI | Meta Global AI Developer Hackathon 2026 | "
    "Synthetic demonstration only | Human-supervised IT support"
)