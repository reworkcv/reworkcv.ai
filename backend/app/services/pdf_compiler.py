"""
PDF compilation service - compiles LaTeX to PDF using pdflatex.
"""
import logging
import subprocess
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class PDFCompilerService:
    """Service for compiling LaTeX documents to PDF."""
    
    def __init__(self):
        """Initialize the PDF compiler."""
        self._check_pdflatex()
    
    def _check_pdflatex(self) -> None:
        """Check if pdflatex is available."""
        if shutil.which("pdflatex") is None:
            logger.warning("pdflatex not found in PATH. PDF compilation may fail.")
    
    def compile(self, latex_content: str, output_path: Path) -> Path:
        """
        Compile LaTeX content to PDF.
        
        Args:
            latex_content: LaTeX document content
            output_path: Path for the output PDF file
            
        Returns:
            Path to the generated PDF file
        """
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write LaTeX to temp file
        tex_file = output_path.with_suffix(".tex")
        tex_file.write_text(latex_content, encoding="utf-8")
        
        logger.info(f"Compiling LaTeX: {tex_file}")
        
        try:
            # Run pdflatex twice for proper references
            for _ in range(2):
                result = subprocess.run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        "-output-directory", str(output_dir),
                        str(tex_file)
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    logger.error(f"pdflatex error: {result.stderr}")
                    logger.error(f"pdflatex output: {result.stdout}")
            
            pdf_path = output_path.with_suffix(".pdf")
            
            if not pdf_path.exists():
                raise RuntimeError(f"PDF file not created: {pdf_path}")
            
            # Clean up auxiliary files
            self._cleanup_aux_files(output_dir, tex_file.stem)
            
            logger.info(f"PDF generated: {pdf_path}")
            return pdf_path
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("pdflatex compilation timed out")
        except Exception as e:
            logger.error(f"PDF compilation failed: {e}")
            raise
    
    def _cleanup_aux_files(self, directory: Path, basename: str) -> None:
        """Remove auxiliary LaTeX files."""
        aux_extensions = [".aux", ".log", ".out", ".toc", ".lof", ".lot"]
        for ext in aux_extensions:
            aux_file = directory / f"{basename}{ext}"
            if aux_file.exists():
                aux_file.unlink()
