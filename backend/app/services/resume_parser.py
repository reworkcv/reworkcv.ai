"""
Resume parsing service - converts Markdown to structured JSON using Gemini.
"""
import json
import logging
from google import genai
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class ResumeParserService:
    """Service for parsing resume markdown into structured JSON."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        settings = get_settings()
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
    
    def parse_to_json(self, markdown_content: str) -> dict:
        """
        Convert markdown resume content to structured JSON using Gemini API.
        
        Args:
            markdown_content: The markdown content of the resume
            
        Returns:
            Dictionary containing structured resume data
        """
        prompt = f"""You are a resume parser. Extract ALL information from the following resume markdown and return it as a well-structured JSON object.

Instructions:
1. Dynamically identify all sections present in the resume (e.g., contact info, experience, education, skills, projects, certifications, etc.)
2. For each section, extract all available information
3. Use appropriate data structures:
   - Use arrays for lists of items (e.g., experience entries, skills, education entries)
   - Use objects for structured data with multiple fields
4. For experience entries, always include: company_name, job_title, dates, and any responsibilities/achievements as an array
5. For education entries, include: institution, degree, field_of_study, dates
6. Preserve all text content - do not summarize or omit any information
7. Use snake_case for all JSON keys
8. If a field has no value, omit it from the output (don't include null values)

Resume Markdown:
{markdown_content}

Return ONLY valid JSON, no additional text or explanation."""
        
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )
        
        return json.loads(response.text)
