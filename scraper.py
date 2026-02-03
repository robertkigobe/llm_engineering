"""Scraper module for fetching website contents."""

import requests
from bs4 import BeautifulSoup


def fetch_website_contents(url: str) -> str:
    """Fetch and extract text content from a URL.

    Args:
        url: The URL to fetch.

    Returns:
        Extracted text content from the page.

    Raises:
        requests.RequestException: On fetch failure.
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    text = soup.get_text(separator="\n", strip=True)
    return text
