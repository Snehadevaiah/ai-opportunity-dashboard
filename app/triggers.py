import json
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def detect_triggers(company_name: str, old_info: str, new_info: str):

    prompt = f"""
You are a business intelligence assistant.

Compare the older and newer information about a company.

Company:
{company_name}

OLDER INFORMATION:
{old_info}

NEWER INFORMATION:
{new_info}

Identify meaningful changes that could create a business opportunity.

Return ONLY valid JSON in this structure:

{{
    "company": "{company_name}",
    "change_detected": true,
    "trigger": "short description of the meaningful change",
    "why_it_matters": "why this change matters for business",
    "recommended_action": "one practical action",
    "urgency": "High"
}}

Rules:
- change_detected must be true or false.
- urgency must be High, Medium, or Low.
- Do not invent facts.
- If there is no meaningful change, set change_detected to false.
- Keep the response concise.
- Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)