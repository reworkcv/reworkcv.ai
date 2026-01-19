"""
LaTeX generation service - converts resume JSON to LaTeX using Gemini.
"""
import json
import logging
from pathlib import Path
from google import genai
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class LaTeXGeneratorService:
    """Service for generating LaTeX documents from resume JSON."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        settings = get_settings()
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
    
    def generate(self, resume_json: dict, latex_template: str) -> str:
        """
        Dynamically convert resume JSON to LaTeX using Gemini API.
        
        Args:
            resume_json: Resume data as dictionary
            latex_template: LaTeX template string
            
        Returns:
            Complete LaTeX document as string
        """
        prompt = f"""You are an expert LaTeX programmer. Your task is to fill a LaTeX resume template with data from a JSON resume.

INSTRUCTIONS:
1. Analyze the provided LaTeX template to understand its structure, custom commands, environments, and sections.
2. Analyze the JSON resume data to understand what information is available.
3. Intelligently map the JSON data to the appropriate sections in the LaTeX template.
4. Generate a complete, compilable LaTeX document.

CRITICAL RULES:
1. PRESERVE the entire LaTeX preamble exactly (documentclass, packages, custom commands, environments).
2. PRESERVE all custom LaTeX commands and environments from the template (e.g., \\documentTitle, \\tinysection, \\headingBf, \\headingIt, resume_list, etc.).
3. ESCAPE all LaTeX special characters in the JSON content: % → \\%, $ → \\$, # → \\#, & → \\&, _ → \\_,  {{ → \\{{, }} → \\}}, ~ → \\textasciitilde{{}}, ^ → \\textasciicircum{{}}.
4. Map JSON sections to template sections intelligently:
   - Name/contact info → document title/header
   - Summary/objective/profile_summary → Summary section
   - Skills/technical_skills → Skills section (use tabular if template uses it)
   - Education → Education section
   - Experience/work_experience → Experience section
   - Awards/achievements → Awards section (only if data exists)
   - Any other sections in JSON → create appropriate sections following template style
5. For arrays of items (like responsibilities), use the template's list environment (e.g., resume_list, itemize).
6. For skills with categories, use the template's format (tabular, lists, etc.).
7. If JSON has fields not in template, add them using the template's styling patterns.
8. If template has sections not in JSON, OMIT those sections entirely.
9. Output MUST be valid, compilable LaTeX - no syntax errors.
10. Do NOT add any explanations or markdown - output ONLY the LaTeX code.

LATEX TEMPLATE:
```latex
{latex_template}
```

RESUME JSON:
```json
{json.dumps(resume_json, indent=2)}
```

Generate the complete LaTeX document now. Output ONLY valid LaTeX code, nothing else."""

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        
        # Clean up response - remove any markdown code blocks if present
        latex_output = response.text
        if latex_output.startswith("```"):
            lines = latex_output.split('\n')
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            latex_output = '\n'.join(lines)
        
        return latex_output
