import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def check_reliability(
    company: str,
    source_a: str,
    source_b: str
):

    prompt = f"""
You are evaluating conflicting information about a company.

Company:
{company}

Source A:
{source_a}

Source B:
{source_b}

Determine:

1. Which source should be preferred?
2. Why?
3. What uncertainty remains?

Return ONLY valid JSON in this format:

{{
    "company": "{company}",
    "preferred_source": "Source A",
    "reason": "Explain why this source is more reliable.",
    "uncertainty": "Explain any remaining uncertainty."
}}

Rules:
- Do not invent facts.
- Compare the information based only on the provided sources.
- Clearly explain the reason for choosing a source.
- Mention uncertainty when the evidence is insufficient.
- Return valid JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.endswith("```"):
        text = text[:-3]

    try:
        return json.loads(text.strip())

    except json.JSONDecodeError:

        return {
            "error": "The AI returned invalid JSON.",
            "raw_response": text
        }