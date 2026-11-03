🏥 WardDesk AI

AI First-Responder for Hospital IT Support

Powered by Meta Muse Spark

WardDesk AI is an AI-assisted incident response prototype designed to help hospital IT support teams assess, prioritise and respond to IT incidents through a human-supervised workflow.

🎯 The Problem

Hospital IT support teams handle incidents involving critical systems, networks, workstations and other IT infrastructure.

Manual incident assessment can slow down prioritisation, troubleshooting and escalation.

💡 Our Solution

WardDesk AI combines Meta Muse Spark with structured IT support workflows to assist IT teams with:

• Incident intake and tracking.
• AI-assisted incident prioritisation.
• Context-aware troubleshooting guidance.
• Simulated diagnostic information.
• Human approval and rejection workflow.
• Downloadable incident escalation notes.

🚀 Key Features

1. AI Incident Assessment

Uses Meta Muse Spark to analyse incident descriptions and recommend an IT priority.

2. IT Troubleshooting Guidance

Provides predefined runbook guidance based on the affected IT system.

3. Simulated Diagnostics

Displays predetermined synthetic diagnostic results for demonstration purposes.

4. Human-Supervised Decisions

IT personnel can review and approve or reject AI recommendations.

5. Escalation Support

Generates downloadable text-based escalation notes.

🧠 Technology Stack

• Python
• Streamlit
• Meta Muse Spark API
• OpenAI Python SDK
• Python-dotenv

🔐 Responsible AI

WardDesk AI is designed around human-supervised decision-making.

• AI recommendations are advisory.
• Human personnel retain decision authority.
• The system does not make clinical or patient-care decisions.
• It does not independently approve, reject or close incidents.
• It does not claim access to live hospital systems.

🛠️ Installation

Clone the repository:

git clone https://github.com/nordstreetofficial-beep/warddesk-ai.git
cd warddesk-ai

Install dependencies:

pip install -r requirements.txt

Create a ".env" file in the project directory:

MODEL_API_KEY=your_meta_api_key

Never publish your ".env" file or API key.

Run WardDesk AI:

python -m streamlit run dashboard.py

⚠️ Prototype Limitations

This is a hackathon demonstration prototype.

• No live hospital system integration.
• No production hospital diagnostics.
• No persistent database.
• Incident data is maintained in Streamlit session state and may be lost when the session or server restarts.
• No automated ticketing-system integration.
• Diagnostic results are simulated.

All demonstration scenarios use fictional information.

🌍 Vision

WardDesk AI explores how AI can support hospital IT operations through faster incident assessment, structured troubleshooting and human-supervised escalation.

Building safer and smarter IT support workflows with AI.