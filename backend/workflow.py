from analyst import run_analyst
from schemas import AnalyzeResponse
from scraper import normalize_url, scrape_site


def analyze_url(url: str) -> AnalyzeResponse:
    normalized = normalize_url(url)
    scrape_result = scrape_site(normalized)
    return run_analyst(scrape_result)
