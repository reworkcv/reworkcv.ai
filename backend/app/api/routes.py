"""
API routes for resume processing.
"""
import logging
import uuid
import shutil
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from ..services.pipeline import ResumePipeline
from ..schemas.resume import ResumeProcessResponse, HealthResponse
from ..core.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", message="Resume Tailoring API is running")


@router.post("/process", response_model=ResumeProcessResponse)
async def process_resume(
    resume: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text"),
    template: Optional[UploadFile] = File(None, description="Optional LaTeX template")
):
    """
    Process a resume with a job description.
    
    - Upload resume (PDF/DOCX)
    - Provide job description
    - Optionally provide custom LaTeX template
    - Returns tailored PDF
    """
    settings = get_settings()
    
    # Create uploads directory
    uploads_dir = settings.uploads_dir
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique ID for this request
    request_id = uuid.uuid4().hex[:8]
    
    try:
        # Save uploaded resume
        resume_ext = Path(resume.filename).suffix.lower()
        if resume_ext not in [".pdf", ".docx", ".doc"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid resume format. Please upload PDF or DOCX."
            )
        
        resume_path = uploads_dir / f"resume_{request_id}{resume_ext}"
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)
        
        # Save template if provided
        template_path = None
        if template:
            template_path = uploads_dir / f"template_{request_id}.tex"
            with open(template_path, "wb") as f:
                shutil.copyfileobj(template.file, f)
        else:
            # Use default template
            template_path = settings.templates_dir / "default.tex"
            if not template_path.exists():
                raise HTTPException(
                    status_code=500,
                    detail="Default template not found. Please provide a template."
                )
        
        # Process resume
        pipeline = ResumePipeline()
        result = pipeline.process(
            resume_path=resume_path,
            job_description=job_description,
            template_path=template_path,
            output_name=f"tailored_{request_id}"
        )
        
        return ResumeProcessResponse(
            success=True,
            message="Resume processed successfully",
            pdf_url=f"/api/download/{request_id}",
            latex_content=Path(result["latex_path"]).read_text(encoding="utf-8"),
            tailored_json=result["tailored_json"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error processing resume")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{request_id}")
async def download_pdf(request_id: str):
    """Download the generated PDF."""
    settings = get_settings()
    pdf_path = settings.output_dir / f"tailored_{request_id}.pdf"
    
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"tailored_resume_{request_id}.pdf"
    )


@router.get("/preview/{request_id}")
async def preview_pdf(request_id: str):
    """Get PDF for preview (inline display)."""
    settings = get_settings()
    pdf_path = settings.output_dir / f"tailored_{request_id}.pdf"
    
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline"}
    )
