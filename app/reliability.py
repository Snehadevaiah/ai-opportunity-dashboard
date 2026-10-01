import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def check_reliability(
    company: str,
    source_a: str,
    source_b: str
):

    prompt = f"""
You are a business research and data reliability assistant.

Two sources provide information about the same company.

Company:
{company}

SOURCE A:
{source_a}

SOURCE B:
{source_b}

Compare the sources and determine which information should be
used for business decision-making.

Return ONLY valid JSON in exactly this structure:

{{
    "company": "{company}",
    "conflict_detected": true,
    "preferred_source": "Source A",
    "reason": "Why this source is more reliable",
    "selected_information": "The information that should be used",
    "uncertainty": "What is still uncertain or needs verification"
}}

Rules:
- conflict_detected must be true or false.
- preferred_source must be Source A, Source B, or "Both".
- Do not invent facts.
- Prefer direct company information over unsupported third-party claims.
- Clearly communicate uncertainty.
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