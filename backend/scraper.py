import requests
from bs4 import BeautifulSoup


def scrape_url(url):
    try:
        # Visit the webpage
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        # Check whether the webpage loaded successfully
        response.raise_for_status()

        # Read the webpage's HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove parts that usually don't contain useful article text
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Extract the page title
        title = soup.title.get_text(strip=True) if soup.title else "Untitled page"

        # Extract readable text from the webpage
        page_text = soup.get_text(separator=" ", strip=True)

        return {
            "url": url,
            "title": title,
            "text": page_text[:30000],
            "error": None
        }

    except requests.RequestException as error:
        # Return an error instead of crashing the whole application
        return {
            "url": url,
            "title": None,
            "text": "",
            "error": str(error)
        }