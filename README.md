AI Opportunity Dashboard

An AI-powered business opportunity research and prioritization dashboard.

The system takes company websites as input, researches the available public information, uses AI to analyze the opportunity, scores companies, identifies relevant personas, generates personalized outreach, detects meaningful changes, handles conflicting information, and presents the top opportunities worth acting on today.

1. Problem

When there are many potential companies to approach, manually researching every company is time-consuming.

This project focuses on answering:

«"Which companies are worth acting on today, why, and who should we approach?"»

Instead of displaying a large list of opportunities, the dashboard reduces the list to the top 5 actionable companies.

---

2. Product Flow

Company Website
      ↓
Public Website Research
      ↓
AI Company Analysis
      ↓
Opportunity Scoring
      ↓
Priority Classification
      ↓
Relevant Persona Identification
      ↓
Personalized Outreach
      ↓
Trigger Detection
      ↓
Data Reliability Check
      ↓
Top 5 Action Dashboard

---

3. Main Features

Company Intelligence

The system researches a company website and extracts available information such as:

- Page title
- Meta description
- Research status
- Research limitations

If a website blocks automated access, the system records the limitation instead of treating missing information as positive evidence.

Opportunity Scoring

Each company receives a score from 0–100.

The scoring framework contains five factors:

Factor| Maximum
Business signal| 25
Potential opportunity| 25
Technology/product fit| 20
Evidence quality| 15
Actionability today| 15
Total| 100

Priority is then assigned:

- High: 70–100
- Medium: 40–69
- Low: 0–39

The score reason is returned so that the ranking is explainable rather than being a black-box number.

---

4. Find the Right Person

The system identifies relevant job personas for each company.

For example:

Primary persona:
Chief Marketing Officer

Secondary personas:
Head of Sales
Chief Customer Officer

The system does not invent a person's name.

Instead, it provides:

- Relevant job titles
- Reasons for selecting the persona
- Search queries
- Verification steps

This keeps the workflow useful while reducing the risk of fabricated contact information.

---

5. Personalized Outreach

The system generates a short first-contact message using:

- Company information
- Business signals
- Recommended persona
- Recommended action

The prompt explicitly prevents the AI from inventing:

- People's names
- Company facts
- Unsupported claims

---

6. Trigger Detection

The "/trigger" endpoint compares older and newer company information.

It identifies:

- Whether a meaningful change occurred
- What changed
- Why the change matters
- Recommended action
- Urgency

Example:

Old:
Company provides CRM software.

New:
Company provides CRM software and launched an AI agent platform.

Trigger:
New AI agent platform launch.

Action:
Evaluate potential automation or integration opportunities.

---

7. Data Reliability

The "/reliability" endpoint compares two information sources.

It determines:

- Whether a conflict exists
- Which source should be preferred
- Why it was preferred
- Which information should be used
- What remains uncertain

The system is instructed to prefer direct company information over unsupported third-party claims and explicitly communicate uncertainty.

---

8. Dashboard

The dashboard focuses on the assignment's final product challenge:

«"Show the most important companies to act on today."»

Instead of showing 100 opportunities, the dashboard displays the top 5 based on priority and score.

Each company shows:

- Company
- Score
- Priority
- Recommended persona
- Why it deserves attention
- Recommended action

---

9. API Endpoints

Home

GET /

Checks whether the application is running.

Research

GET /research?website=<company-url>

Researches the company website.

Analyze

GET /analyze?website=<company-url>

Researches and analyzes a company, then saves the result.

Companies

GET /companies
POST /companies

Reads and stores company records.

Top Actions

GET /top-actions

Returns the top 5 companies to act on.

Dashboard

GET /dashboard

Displays the visual dashboard.

Find Right Person

GET /people?website=<company-url>

Identifies relevant personas and search/verification guidance.

Personalized Outreach

GET /outreach?website=<company-url>

Generates a contextual outreach message.

Trigger Detection

GET /trigger

Compares old and new company information.

Reliability

GET /reliability

Compares conflicting sources and communicates uncertainty.

---

10. Technology Stack

- Python
- FastAPI
- Google Gemini API
- Pydantic
- Requests
- BeautifulSoup
- JSON-based local storage
- HTML/CSS dashboard

---

11. AI Model

The project uses:

Gemini 3.5 Flash Lite

AI is used for:

- Company analysis
- Opportunity scoring
- Persona identification
- Personalized outreach
- Trigger detection
- Reliability analysis

The API key is loaded from an environment variable rather than being hard-coded.

---

12. Project Structure

ai-opportunity-dashboard/
│
├── main.py
│
├── app/
│   ├── analysis.py
│   ├── config.py
│   ├── models.py
│   ├── research.py
│   ├── triggers.py
│   ├── reliability.py
│   └── __init__.py
│
├── data/
│   └── opportunities.json
│
├── .env
│
├── venv/
│
└── README.md

---

13. Setup

Create and activate a virtual environment:

python -m venv venv

Windows:

venv\Scripts\activate

Install dependencies:

pip install fastapi uvicorn requests beautifulsoup4 python-dotenv google-genai

Create a ".env" file:

GEMINI_API_KEY=actual_api_key_here

Do not commit the actual API key to GitHub.

---

14. Run the Application

Start the FastAPI server:

uvicorn main:app --reload

Open:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

Dashboard:

http://127.0.0.1:8000/dashboard

---

15. Example Workflow

Start with a company:

/analyze?website=https://www.hubspot.com

Then find the relevant persona:

/people?website=https://www.hubspot.com

Generate personalized outreach:

/outreach?website=https://www.hubspot.com

Finally view the prioritized opportunities:

/dashboard

---

16. Reliability and Limitations

The system is intentionally designed not to assume that missing information is positive evidence.

Potential limitations include:

- Websites may block automated requests.
- Public website information can be incomplete.
- AI-generated analysis can contain uncertainty.
- Actual employee identities should be verified using current public professional/company sources.
- The current database is a lightweight JSON store intended for the take-home project rather than production-scale deployment.

These limitations are surfaced instead of being hidden from the user.

---

17. Assignment Requirement Mapping

Assignment Requirement| Implementation
Company Intelligence| "/research" + "/analyze"
Opportunity Scoring| 100-point scoring framework
Find the Right Person| "/people"
Personalized Outreach| "/outreach"
Automation| Research → AI → structured result → database
Trigger Detection| "/trigger"
Data Reliability| "/reliability"
Open-ended Product Challenge| "/dashboard"
Requirement Change: 100 → 5| "/top-actions" + dashboard

---

18. Product Thinking

The main product decision is to prioritize actionability over volume.

Rather than giving the user another large list of companies, the dashboard answers three practical questions:

1. Which companies deserve attention?
2. Why should I act?
3. Who should I approach?

This reduces the amount of manual research required before taking the next action.