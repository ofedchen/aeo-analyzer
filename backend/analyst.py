from __future__ import annotations

import json
import os
import re

from crewai import Agent, Crew, LLM, Process, Task

from schemas import Analysis, AnalyzeResponse, Metrics, Protocols
from scraper import ScrapeResult, scrape_summary_for_llm


def _build_llm() -> LLM:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy backend/.env.example to backend/.env "
            "and add your Google AI Studio key."
        )
    return LLM(model="gemini/gemini-2.0-flash", api_key=api_key, temperature=0.2)


def _heuristic_score(result: ScrapeResult) -> int:
    score = 35
    if result.page_title:
        score += 10
    if result.meta_description:
        score += 10
    if result.json_ld_found:
        score += 20
    if result.llms_txt_found:
        score += 20
    if len(result.visible_text) > 500:
        score += 5
    if len(result.visible_text) > 2000:
        score += 5
    if result.fetch_error:
        score = min(score, 25)
    return min(score, 100)


def _fallback_analysis(result: ScrapeResult) -> Analysis:
    items: list[str] = []
    if not result.llms_txt_found:
        items.append(
            "Publish a /llms.txt file describing site purpose, key pages, and usage guidelines for LLMs."
        )
    if not result.json_ld_found:
        items.append(
            "Add JSON-LD structured data (Organization, WebSite, or Product) in the homepage head."
        )
    if not result.meta_description:
        items.append("Add a concise meta description that summarizes the page for retrieval systems.")
    if not result.page_title:
        items.append("Set a descriptive HTML title tag with primary entity and intent keywords.")
    if len(result.visible_text) < 500:
        items.append(
            "Increase machine-readable text content; thin pages score poorly for RAG and AI search."
        )
    if not items:
        items.append(
            "Maintain llms.txt and JSON-LD as content changes; audit quarterly for schema drift."
        )

    summary = (
        "Automated fallback analysis (LLM unavailable). "
        f"Protocols: llms.txt={'present' if result.llms_txt_found else 'missing'}, "
        f"JSON-LD={'present' if result.json_ld_found else 'missing'}."
    )
    return Analysis(summary=summary, action_items=items)


def _extract_json_object(text: str) -> dict:
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    else:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]
    return json.loads(text)


def run_analyst(result: ScrapeResult) -> AnalyzeResponse:
    crawl_payload = scrape_summary_for_llm(result)
    protocols = Protocols(
        llms_txt_found=result.llms_txt_found,
        json_ld_found=result.json_ld_found,
    )

    try:
        llm = _build_llm()
    except RuntimeError:
        return AnalyzeResponse(
            target_url=result.final_url,
            protocols=protocols,
            metrics=Metrics(legibility_score=_heuristic_score(result)),
            analysis=_fallback_analysis(result),
        )

    scraper_agent = Agent(
        role="Technical Crawler",
        goal="Validate and summarize crawl artifacts for downstream AEO analysis.",
        backstory=(
            "You are a web crawling specialist focused on machine-readable site signals "
            "such as llms.txt, JSON-LD, and clean text extraction."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    analyst_agent = Agent(
        role="AEO Strategist",
        goal="Score AI search readiness and produce actionable optimization recommendations.",
        backstory=(
            "You are an Answer Engine Optimization expert who evaluates websites for "
            "LLM retrieval, citation, and structured understanding."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    crawl_task = Task(
        description=(
            "Review the crawl payload below and produce a concise technical brief "
            "highlighting llms.txt status, JSON-LD coverage, metadata quality, and text legibility.\n\n"
            f"{crawl_payload}"
        ),
        expected_output="A structured technical brief of crawl findings.",
        agent=scraper_agent,
    )

    analysis_task = Task(
        description=(
            "Using the technical brief from the crawler, evaluate AI search readiness.\n"
            "Return ONLY valid JSON matching this exact schema (no markdown, no commentary):\n"
            "{\n"
            '  "legibility_score": <integer 0-100>,\n'
            '  "summary": "<2-3 sentence executive summary>",\n'
            '  "action_items": ["<specific recommendation>", "..."]\n'
            "}\n\n"
            "Scoring guidance:\n"
            "- Reward llms.txt, JSON-LD, clear metadata, and substantial readable text.\n"
            "- Penalize missing protocols, thin content, and noisy markup-heavy pages.\n"
            "- Provide 3-6 concrete, prioritized action items."
        ),
        expected_output="Valid JSON with legibility_score, summary, and action_items.",
        agent=analyst_agent,
        context=[crawl_task],
    )

    crew = Crew(
        agents=[scraper_agent, analyst_agent],
        tasks=[crawl_task, analysis_task],
        process=Process.sequential,
        verbose=False,
    )

    try:
        raw_output = str(crew.kickoff())
        parsed = _extract_json_object(raw_output)
        score = int(parsed.get("legibility_score", _heuristic_score(result)))
        score = max(0, min(score, 100))
        summary = str(parsed.get("summary", "")).strip() or _fallback_analysis(result).summary
        action_items = parsed.get("action_items") or _fallback_analysis(result).action_items
        if isinstance(action_items, str):
            action_items = [action_items]
        action_items = [str(item).strip() for item in action_items if str(item).strip()]
        if not action_items:
            action_items = _fallback_analysis(result).action_items

        return AnalyzeResponse(
            target_url=result.final_url,
            protocols=protocols,
            metrics=Metrics(legibility_score=score),
            analysis=Analysis(summary=summary, action_items=action_items),
        )
    except Exception:
        return AnalyzeResponse(
            target_url=result.final_url,
            protocols=protocols,
            metrics=Metrics(legibility_score=_heuristic_score(result)),
            analysis=_fallback_analysis(result),
        )
