from pydantic import BaseModel, Field


class Protocols(BaseModel):
    llms_txt_found: bool
    json_ld_found: bool


class Metrics(BaseModel):
    legibility_score: int = Field(ge=0, le=100)


class Analysis(BaseModel):
    summary: str
    action_items: list[str]


class AnalyzeResponse(BaseModel):
    target_url: str
    protocols: Protocols
    metrics: Metrics
    analysis: Analysis
