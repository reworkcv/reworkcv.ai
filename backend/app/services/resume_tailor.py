"""
Resume tailoring service - adapts resume JSON to match job descriptions using Gemini.
"""
import json
import logging
from google import genai
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class ResumeTailorService:
    """Service for tailoring resume content to job descriptions."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        settings = get_settings()
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
    
    def tailor(self, resume_json: dict, job_description: str) -> dict:
        """
        Tailor resume JSON to match a job description using Gemini API.
        
        Args:
            resume_json: The original resume as a dictionary
            job_description: The job description text
            
        Returns:
            Dictionary containing tailored resume data with same structure
        """
        prompt = f"""You are an expert resume tailor and JSON editor with extensive experience in adapting resumes for specific job descriptions in the tech industry, particularly AI and data engineering roles. Your task is to take the provided resume in JSON format and rewrite its content to better align with the given job description. You must emphasize skills, experiences, and responsibilities that match the job's requirements.

IMPORTANT RULES - FOLLOW THESE EXACTLY:
1. Keep the entire JSON structure identical: Do not add, remove, or rename any keys. Do not change the overall format, arrays, or objects. For example, if a key is "profile_summary" and it's an array, keep it as an array; if "technical_skills" is an object with sub-keys, keep those sub-keys the same.
2. Only modify the values (the content inside the keys) to make them more relevant to the job description. Rewrite sentences to incorporate job-specific terms while keeping the core facts from the original resume plausible and truthful.
3. For "profile_summary" or "summary": Rewrite to highlight relevant aspects mentioned in the job description. Keep it concise and professional.
4. For "education": Keep unchanged, as it's factual and not experience-based.
5. For "technical_skills" or "skills": Update by adding or rephrasing items to include job-relevant tools and technologies mentioned in the job description. Do not remove existing items; only enhance or rephrase for relevance.
6. For "work_experience" or "experience": For each job entry:
   - Keep "company_name", "job_title", "dates" unchanged.
   - Rewrite "responsibilities_achievements" or "responsibilities" array: Rephrase each bullet to align with job responsibilities. Emphasize relevant technologies and methodologies.
   - Rewrite "environment" if present: Update the list of tools to prioritize job matches.
7. Make all rewritten content professional, achievement-oriented, and quantifiable where possible (e.g., "improved efficiency by 50%"). Ensure it sounds natural and not forced.
8. Output ONLY the rewritten JSON. Do not include any explanations, introductions, or extra text. The output must be valid JSON that parses perfectly.

Job Description:
{job_description}

Original Resume JSON:
{json.dumps(resume_json, indent=2)}

Return ONLY valid JSON with the exact same structure as the input."""
        
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )
        
        return json.loads(response.text)
