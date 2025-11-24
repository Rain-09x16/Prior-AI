"""
Document parser service for extracting text from PDF and DOCX files.
"""
from typing import Optional
import PyPDF2
from docx import Document
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class DocumentParser:
    """Parse PDF and DOCX files to extract text."""

    def parse(self, file_path: str, file_type: str) -> str:
        """
        Parse document and return full text.

        Args:
            file_path: Path to the document file
            file_type: Type of file ('pdf' or 'docx')

        Returns:
            Extracted text from the document

        Raises:
            ValueError: If file type is not supported
            Exception: If parsing fails
        """
        logger.info(f"Parsing {file_type} file: {file_path}")

        try:
            if file_type == 'pdf':
                return self._parse_pdf(file_path)
            elif file_type == 'docx':
                return self._parse_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            logger.error(f"Failed to parse document: {str(e)}")
            raise

    def _parse_pdf(self, file_path: str) -> str:
        """
        Parse PDF file and extract text.

        Args:
            file_path: Path to PDF file

        Returns:
            Extracted text
        """
        text = ""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                logger.info(f"PDF has {num_pages} pages")

                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    logger.debug(f"Extracted text from page {page_num}/{num_pages}")

            logger.info(f"Successfully extracted {len(text)} characters from PDF")
            return text.strip()

        except Exception as e:
            logger.error(f"PDF parsing error: {str(e)}")
            raise Exception(f"Failed to parse PDF: {str(e)}")

    def _parse_docx(self, file_path: str) -> str:
        """
        Parse DOCX file and extract text.

        Args:
            file_path: Path to DOCX file

        Returns:
            Extracted text
        """
        try:
            doc = Document(file_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
            text = "\n".join(paragraphs)

            logger.info(f"Successfully extracted {len(text)} characters from DOCX ({len(paragraphs)} paragraphs)")
            return text.strip()

        except Exception as e:
            logger.error(f"DOCX parsing error: {str(e)}")
            raise Exception(f"Failed to parse DOCX: {str(e)}")

    def extract_title(self, text: str, filename: str) -> str:
        """
        Extract title from document text or use filename as fallback.

        Args:
            text: Document text
            filename: Original filename

        Returns:
            Extracted or generated title
        """
        # Try to extract first non-empty line as title
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Use first line if it's not too long (likely a title)
            first_line = lines[0]
            if len(first_line) <= 200:
                return first_line

        # Fallback to filename without extension
        return filename.rsplit('.', 1)[0]
