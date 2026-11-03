import os
from dotenv import load_dotenv
from openai import OpenAI

# Load private API key from .env
load_dotenv()

api_key = os.getenv("MODEL_API_KEY")

if not api_key:
    print("ERROR: API key not found. Check your .env file.")
    raise SystemExit(1)

# Connect to Meta Model API
client = OpenAI(
    base_url="https://api.meta.ai/v1",
    api_key=api_key
)

print("Connecting to Meta Muse Spark...")

try:
    response = client.responses.create(
        model="muse-spark-1.3",
        input="""
        You are WardDesk, a hospital administrative assistant.

        Prioritise these fictional tasks:
        A. Discharge paperwork due in 30 minutes.
        B. Supply reorder due tomorrow.
        C. Room cleaning needed in 20 minutes.

        Explain your priority order.
        Do not make clinical decisions.
        Require human approval.
        """
    )

    print("\n===== WARDDESK AI RESPONSE =====\n")
    print(response.output_text)
    print("\n===== CONNECTION SUCCESSFUL =====")

except Exception as error:
    print("\nAPI CONNECTION ERROR:")
    print(error)