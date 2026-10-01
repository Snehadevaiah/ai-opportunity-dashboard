import requests
from bs4 import BeautifulSoup


def research_company(website: str):
    try:
        response = requests.get(
            website,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )

        # Website blocked the request
        if response.status_code == 403:
            return {
                "title": website,
                "description": "",
                "research_status": "blocked",
                "research_note": "The website blocked automated access."
            }

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""

        description_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        description = (
            description_tag.get("content", "").strip()
            if description_tag
            else ""
        )

        return {
            "title": title,
            "description": description,
            "research_status": "success",
            "research_note": ""
        }

    except requests.RequestException as error:
        return {
            "title": website,
            "description": "",
            "research_status": "error",
            "research_note": f"Website research failed: {str(error)}"
        }