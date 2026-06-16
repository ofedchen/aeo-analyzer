from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; AEOValidator/1.0; +https://github.com/aeo-validator)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
REQUEST_TIMEOUT = 20


@dataclass
class ScrapeResult:
    target_url: str
    final_url: str
    page_title: str = ""
    meta_description: str = ""
    visible_text: str = ""
    json_ld_blocks: list[dict] = field(default_factory=list)
    json_ld_found: bool = False
    llms_txt_found: bool = False
    llms_txt_content: str = ""
    llms_txt_url: str = ""
    fetch_error: str | None = None


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("URL is required")
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = f"https://{url}"
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid URL")
    return url


def _extract_json_ld(soup: BeautifulSoup) -> list[dict]:
    blocks: list[dict] = []
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text()
        if not raw or not raw.strip():
            continue
        try:
            parsed = json.loads(raw.strip())
            if isinstance(parsed, list):
                blocks.extend(item for item in parsed if isinstance(item, dict))
            elif isinstance(parsed, dict):
                blocks.append(parsed)
        except json.JSONDecodeError:
            continue
    return blocks


def _extract_visible_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:200])


def fetch_llms_txt(base_url: str, session: requests.Session) -> tuple[bool, str, str]:
    parsed = urlparse(base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    candidates = [
        urljoin(origin, "/llms.txt"),
        urljoin(origin, "/.well-known/llms.txt"),
    ]
    for candidate in candidates:
        try:
            response = session.get(candidate, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200 and response.text.strip():
                return True, response.text.strip(), candidate
        except requests.RequestException:
            continue
    return False, "", ""


def scrape_site(url: str) -> ScrapeResult:
    normalized = normalize_url(url)
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    result = ScrapeResult(target_url=normalized, final_url=normalized)

    try:
        response = session.get(normalized, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        response.raise_for_status()
        result.final_url = response.url
    except requests.RequestException as exc:
        result.fetch_error = str(exc)
        return result

    soup = BeautifulSoup(response.text, "lxml")
    title_tag = soup.find("title")
    result.page_title = title_tag.get_text(strip=True) if title_tag else ""

    meta_desc = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    if meta_desc and meta_desc.get("content"):
        result.meta_description = meta_desc["content"].strip()

    result.json_ld_blocks = _extract_json_ld(soup)
    result.json_ld_found = len(result.json_ld_blocks) > 0
    result.visible_text = _extract_visible_text(soup)

    llms_found, llms_content, llms_url = fetch_llms_txt(result.final_url, session)
    result.llms_txt_found = llms_found
    result.llms_txt_content = llms_content
    result.llms_txt_url = llms_url

    return result


def scrape_summary_for_llm(result: ScrapeResult) -> str:
    json_ld_preview = json.dumps(result.json_ld_blocks[:3], indent=2)[:4000]
    llms_preview = result.llms_txt_content[:2000] if result.llms_txt_content else "(not found)"
    text_preview = result.visible_text[:6000]

    return f"""Target URL: {result.final_url}
Page title: {result.page_title or "(missing)"}
Meta description: {result.meta_description or "(missing)"}

Protocol checks:
- llms.txt found: {result.llms_txt_found}
- llms.txt URL: {result.llms_txt_url or "(n/a)"}
- JSON-LD found: {result.json_ld_found}
- JSON-LD block count: {len(result.json_ld_blocks)}

llms.txt preview:
{llms_preview}

JSON-LD preview:
{json_ld_preview}

Visible page text preview:
{text_preview}
"""
