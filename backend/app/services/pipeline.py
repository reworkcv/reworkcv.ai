"""
Resume processing pipeline - orchestrates the full resume tailoring workflow.
"""
import logging
import uuid
from pathlib import Path
from typing import Optional

from .document_converter import DocumentConverterService
from .resume_parser import ResumeParserService
from .resume_tailor import ResumeTailorService
from .latex_generator import LaTeXGeneratorService
from .pdf_compiler import PDFCompilerService
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class ResumePipeline:
    """Orchestrates the complete resume tailoring pipeline."""
    
    def __init__(self):
        """Initialize all services."""
        self._converter = DocumentConverterService()
        self._parser = ResumeParserService()
        self._tailor = ResumeTailorService()
        self._latex_gen = LaTeXGeneratorService()
        self._pdf_compiler = PDFCompilerService()
        self._settings = get_settings()
    
    def process(
        self,
        resume_path: Path,
        job_description: str,
        template_path: Optional[Path] = None,
        output_name: Optional[str] = None
    ) -> dict:
        """
        Process a resume through the complete pipeline.
        
        Args:
            resume_path: Path to the resume file (PDF, DOCX, etc.)
            job_description: Job description text
            template_path: Optional path to LaTeX template
            output_name: Optional name for output files
            
        Returns:
            Dictionary with processing results
        """
        if output_name is None:
            output_name = f"resume_{uuid.uuid4().hex[:8]}"
        
        output_dir = self._settings.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Convert document to markdown
        logger.info("Step 1: Converting document to markdown...")
        markdown_content = self._converter.convert_to_markdown(resume_path)
        
        # Step 2: Parse markdown to JSON
        logger.info("Step 2: Parsing markdown to JSON...")
        resume_json = self._parser.parse_to_json(markdown_content)
        
        # Step 3: Tailor resume to job description
        logger.info("Step 3: Tailoring resume to job description...")
        tailored_json = self._tailor.tailor(resume_json, job_description)
        
        # Step 4: Generate LaTeX
        logger.info("Step 4: Generating LaTeX...")
        if template_path is None:
            template_path = self._settings.templates_dir / "default.tex"
        
        latex_template = template_path.read_text(encoding="utf-8")
        latex_content = self._latex_gen.generate(tailored_json, latex_template)
        
        # Save LaTeX file
        latex_path = output_dir / f"{output_name}.tex"
        latex_path.write_text(latex_content, encoding="utf-8")
        
        # Step 5: Compile to PDF
        logger.info("Step 5: Compiling to PDF...")
        pdf_path = self._pdf_compiler.compile(latex_content, output_dir / output_name)
        
        return {
            "success": True,
            "output_name": output_name,
            "pdf_path": str(pdf_path),
            "latex_path": str(latex_path),
            "tailored_json": tailored_json
        }
