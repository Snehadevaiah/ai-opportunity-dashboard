from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.models import Company
from app.research import research_company
from app.analysis import analyze_company, client
from app.triggers import detect_triggers
from app.reliability import check_reliability

import json
from pathlib import Path


app = FastAPI(title="AI Opportunity Dashboard")

DATA_FILE = Path("data/opportunities.json")


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Opportunity Dashboard is running!"
    }


# --------------------------------------------------
# CREATE COMPANY
# --------------------------------------------------

@app.post("/companies")
def create_company(company: Company):

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    companies.append(company.model_dump())

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(companies, file, indent=4)

    return {
        "message": "Company saved successfully",
        "company": company
    }


# --------------------------------------------------
# GET ALL COMPANIES
# --------------------------------------------------

@app.get("/companies")
def get_companies():

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    return {
        "count": len(companies),
        "companies": companies
    }


# --------------------------------------------------
# RESEARCH COMPANY
# --------------------------------------------------

@app.get("/research")
def research(website: str):

    return research_company(website)


# --------------------------------------------------
# ANALYZE COMPANY
# --------------------------------------------------

@app.get("/analyze")
def analyze(website: str):

    research_data = research_company(website)

    analysis = analyze_company(research_data)

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    company_data = analysis.model_dump()
    company_data["website"] = website

    existing_index = next(
        (
            i
            for i, company in enumerate(companies)
            if company.get("website") == website
        ),
        None
    )

    if existing_index is not None:
        companies[existing_index].update(company_data)
    else:
        companies.append(company_data)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(companies, file, indent=4)

    return analysis


# --------------------------------------------------
# TOP 5 ACTIONS
# --------------------------------------------------

@app.get("/top-actions")
def top_actions():

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    priority_order = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    companies.sort(
        key=lambda company: (
            priority_order.get(
                company.get("priority", "Low"),
                1
            ),
            company.get("score", 0)
        ),
        reverse=True
    )

    top_companies = companies[:5]

    actions = []

    for company in top_companies:

        actions.append({
            "company_name": company.get("company_name"),
            "website": company.get("website"),
            "score": company.get("score"),
            "priority": company.get("priority"),
            "why_act_today": company.get("score_reason"),
            "recommended_action": company.get("recommended_action")
        })

    return {
        "count": len(actions),
        "top_actions": actions
    }


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    priority_order = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    companies.sort(
        key=lambda company: (
            priority_order.get(
                company.get("priority", "Low"),
                1
            ),
            company.get("score", 0)
        ),
        reverse=True
    )

    top_companies = companies[:5]

    rows = ""

    for company in top_companies:

        rows += f"""
        <tr>

            <td>
                <strong>
                    {company.get("company_name", "Unknown")}
                </strong>

                <br><br>

                <a href="{company.get("website", "#")}"
                   target="_blank">
                    Visit Website
                </a>
            </td>

            <td>
                <strong>
                    {company.get("score", 0)}
                </strong>/100
            </td>

            <td>
                <strong>
                    {company.get("priority", "Unknown")}
                </strong>
            </td>

            <td>
                {company.get(
                    "recommended_persona",
                    "Not available"
                )}
            </td>

            <td>
                {company.get(
                    "score_reason",
                    "No reason available"
                )}
            </td>

            <td>
                {company.get(
                    "recommended_action",
                    "Not available"
                )}
            </td>

        </tr>
        """

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>AI Opportunity Dashboard</title>

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <style>

            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 30px;
                background: #f5f7fa;
                color: #222;
            }}

            .container {{
                max-width: 1600px;
                margin: auto;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .subtitle {{
                color: #666;
                margin-bottom: 25px;
            }}

            .card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                overflow-x: auto;
            }}

            table {{
                width: 100%;
                min-width: 1200px;
                border-collapse: collapse;
            }}

            th {{
                background: #222;
                color: white;
                padding: 14px;
                text-align: left;
                white-space: nowrap;
            }}

            td {{
                padding: 14px;
                border-bottom: 1px solid #ddd;
                vertical-align: top;
                line-height: 1.5;
            }}

            tr:hover {{
                background: #f8f8f8;
            }}

            a {{
                color: #2563eb;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            .empty {{
                padding: 30px;
                text-align: center;
                color: #666;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>
                AI Opportunity Dashboard
            </h1>

            <div class="subtitle">
                Top 5 companies worth acting on today
            </div>

            <div class="card">

                <table>

                    <thead>

                        <tr>

                            <th>Company</th>
                            <th>Score</th>
                            <th>Priority</th>
                            <th>Recommended Persona</th>
                            <th>Why Act Today</th>
                            <th>Recommended Action</th>

                        </tr>

                    </thead>

                    <tbody>

                        {rows if rows else '''
                        <tr>
                            <td colspan="6" class="empty">
                                No companies analyzed yet.
                            </td>
                        </tr>
                        '''}

                    </tbody>

                </table>

            </div>

        </div>

    </body>

    </html>
    """

    return HTMLResponse(content=html)


# --------------------------------------------------
# FIND THE RIGHT PERSON
# --------------------------------------------------

@app.get("/people")
def find_right_person(website: str):

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    company = next(
        (
            item
            for item in companies
            if item.get("website") == website
        ),
        None
    )

    if not company:
        return {
            "error": "Company not found. Analyze the company first."
        }

    company_name = company.get(
        "company_name",
        "Unknown company"
    )

    persona = company.get(
        "recommended_persona",
        ""
    )

    persona_reason = company.get(
        "persona_reason",
        ""
    )

    recommended_action = company.get(
        "recommended_action",
        ""
    )

    prompt = f"""
You are a B2B business research assistant.

Your task is to identify the most relevant PERSONA
to approach at the company.

Company:
{company_name}

Recommended persona from previous analysis:
{persona}

Reason:
{persona_reason}

Recommended action:
{recommended_action}


Return ONLY valid JSON.

Use exactly this structure:

{{
    "company": "{company_name}",
    "primary_persona": "one specific job title",
    "secondary_personas": [
        "one job title",
        "one job title"
    ],
    "why_primary_persona": "one clear sentence explaining why this role is relevant",
    "search_queries": [
        "{company_name} [primary job title]",
        "{company_name} [relevant department] leader",
        "site:linkedin.com/in {company_name} [primary job title]"
    ],
    "verification_steps": [
        "Check that the person currently works at the company",
        "Check that the person owns the relevant function",
        "Verify the role using a public company or professional profile"
    ]
}}


STRICT RULES:

1. Do NOT invent a person's name.

2. Do NOT claim that a specific person works at
the company.

3. primary_persona must contain ONLY a job title.
Do not add explanations to this field.

4. secondary_personas must contain ONLY job titles.

5. why_primary_persona must be one clear sentence.

6. search_queries must be complete, useful search queries.
Do not abbreviate words.

7. Do not produce malformed or incomplete words.

8. verification_steps must be complete sentences.

9. Keep the response concise.

10. Return valid JSON only.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        result = json.loads(text)

    except json.JSONDecodeError:

        return {
            "error": "The AI returned invalid JSON. Please try again.",
            "raw_response": text
        }

    return result


# --------------------------------------------------
# PERSONALISED OUTREACH
# --------------------------------------------------

@app.get("/outreach")
def outreach(website: str):

    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
    else:
        companies = []

    company = next(
        (
            item
            for item in companies
            if item.get("website") == website
        ),
        None
    )

    if not company:
        return {
            "error": "Company not found. Analyze the company first."
        }

    prompt = f"""
You are a B2B business development assistant.

Create a short, personalized first outreach message
for the company below.

Company:
{company.get("company_name")}

Summary:
{company.get("summary")}

Business signals:
{company.get("signals")}

Recommended persona:
{company.get("recommended_persona")}

Recommended action:
{company.get("recommended_action")}

Rules:
- Keep it under 100 words.
- Make it specific to the available company information.
- Do not invent a person's name.
- Do not invent company facts.
- Do not use generic phrases like "I hope you're doing well".
- Do not make unsupported claims.
- Make it sound like a human first message.
- Check spelling and grammar carefully.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return {
        "company": company.get("company_name"),
        "persona": company.get("recommended_persona"),
        "message": response.text.strip()
    }


# --------------------------------------------------
# TRIGGER DETECTION
# --------------------------------------------------

@app.get("/trigger")
def trigger(
    company: str,
    old_info: str,
    new_info: str
):

    result = detect_triggers(
        company_name=company,
        old_info=old_info,
        new_info=new_info
    )

    return result


# --------------------------------------------------
# DATA RELIABILITY
# --------------------------------------------------

@app.get("/reliability")
def reliability(
    company: str,
    source_a: str,
    source_b: str
):

    result = check_reliability(
        company=company,
        source_a=source_a,
        source_b=source_b
    )

    return result