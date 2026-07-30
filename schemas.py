from typing import List, Optional
from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict, Any

class LeadInfo(BaseModel):
    company_name: str = Field(description="Official name of the company")
    industry: str = Field(description="Primary industry they operate in")
    tech_stack: List[str] = Field(description="List of technologies they likely use (e.g. Python, React)")
    pain_points: List[str] = Field(description="Current challenges or news that suggest a need for your service")

class Evaluation(BaseModel):
    score: int = Field(description="Fit score from 0 to 100")
    is_qualified: bool = Field(description="True if score > 70, otherwise False")
    reasoning: str = Field(description="Brief explanation of why they are or aren't a fit")

class OutreachDraft(BaseModel):
    subject_line: str
    email_body: str

class AgentState(TypedDict):
    raw_input: str

    lead_data: dict  

    evaluation: dict 

    draft_email: dict 

    errors: List[str]