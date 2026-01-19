"""
Pydantic schemas for resume-related requests and responses.
"""
from pydantic import BaseModel
from typing import Optional, Any


class ResumeProcessRequest(BaseModel):
    """Request schema for processing resume with job description."""
    job_description: str


class ResumeProcessResponse(BaseModel):
    """Response schema for processed resume."""
    success: bool
    message: str
    pdf_url: Optional[str] = None
    latex_content: Optional[str] = None
    tailored_json: Optional[dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str
