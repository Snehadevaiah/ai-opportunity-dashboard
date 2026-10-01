import os
import json

from dotenv import load_dotenv
from google import genai

from app.models import CompanyAnalysis


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_company(research_data: dict) -> CompanyAnalysis:

    title = research_data.get("title", "")
    description = research_data.get("description", "")

    research_status = research_data.get(
        "research_status",
        "unknown"
    )

    research_note = research_data.get(
        "research_note",
        ""
    )

    prompt = f"""
You are a business research and opportunity scoring assistant.

Analyze the company using ONLY the information provided below.

Company:
{title}

Website description:
{description}

Research status:
{research_status}

Research note:
{research_note}


SCORING FRAMEWORK

Evaluate the opportunity using these five factors:

1. Business signal: 0-25
2. Potential opportunity: 0-25
3. Technology/product fit: 0-20
4. Evidence quality: 0-15
5. Actionability today: 0-15

The final score must be:

business signal
+ potential opportunity
+ technology/product fit
+ evidence quality
+ actionability today

Maximum = 100.


Return ONLY valid JSON in exactly this structure:

{{
    "company_name": "string",

    "summary": "short company summary",

    "signals": [
        "business signal 1",
        "business signal 2",
        "business signal 3"
    ],

    "score": 0,

    "score_reason": "Explain the score using the five scoring factors.",

    "priority": "High",

    "recommended_persona": "relevant role or persona to approach",

    "persona_reason": "Why this persona is relevant.",

    "recommended_action": "One practical next action.",

    "uncertainty": "What information is missing or uncertain."
}}


Rules:

- Score must be between 0 and 100.
- Use the scoring framework above.
- Priority must be High, Medium, or Low.
- High = 70-100.
- Medium = 40-69.
- Low = 0-39.
- Do not invent specific people.
- Do not invent company facts.
- If the website was blocked or information is missing,
  reduce the evidence quality and clearly mention the limitation.
- Do not treat missing information as positive evidence.
- Use only the provided research.
- Keep the response concise.
- Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    ai_text = response.text.strip()

    if ai_text.startswith("```"):
        ai_text = (
            ai_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    data = json.loads(ai_text)

    return CompanyAnalysis(**data)