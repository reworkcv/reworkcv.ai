"""
Document to Markdown conversion service using Docling.
"""
import logging
from pathlib import Path
from typing import Optional

try:
    from docling.document_converter import DocumentConverter
except ImportError:
    DocumentConverter = None

logger = logging.getLogger(__name__)


class DocumentConverterService:
    """Service for converting documents (PDF, DOCX) to Markdown."""
    
    def __init__(self):
        """Initialize the document converter."""
        if DocumentConverter is None:
            raise ImportError("docling package not found. Install with: pip install docling")
        self._converter = DocumentConverter()
        logger.info("Document converter initialized")
    
    def convert_to_markdown(self, source_path: str | Path) -> str:
        """
        Convert a document to Markdown format.
        
        Args:
            source_path: Path to local file
            
        Returns:
            Markdown content as string
        """
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        logger.info(f"Converting document: {source_path}")
        result = self._converter.convert(str(source_path))
        markdown_content = result.document.export_to_markdown()
        
        return markdown_content
    
    def convert_and_save(
        self, 
        source_path: str | Path, 
        output_path: Optional[str | Path] = None
    ) -> str:
        """
        Convert document and optionally save to file.
        
        Args:
            source_path: Path to source document
            output_path: Optional path to save markdown output
            
        Returns:
            Markdown content as string
        """
        markdown_content = self.convert_to_markdown(source_path)
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(markdown_content, encoding="utf-8")
            logger.info(f"Markdown saved to: {output_path}")
        
        return markdown_content
