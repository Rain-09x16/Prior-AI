"""File handling utilities."""
import os
import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings


class FileHandler:
    """Handle file uploads and storage."""

    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Validate uploaded file."""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )

    @staticmethod
    async def save_file(file: UploadFile, directory: Path) -> Tuple[str, str]:
        """
        Save uploaded file to disk.

        Returns:
            Tuple of (original_filename, saved_file_path)
        """
        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = directory / unique_filename

        # Save file
        try:
            content = await file.read()

            # Check file size
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
                )

            with open(file_path, "wb") as f:
                f.write(content)

            return file.filename, str(file_path)

        except Exception as e:
            # Clean up partial file if exists
            if file_path.exists():
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    @staticmethod
    def delete_file(file_path: str) -> None:
        """Delete file from disk."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete file {file_path}: {str(e)}")

    @staticmethod
    def get_file_type(filename: str) -> str:
        """Get file type from filename."""
        return Path(filename).suffix.lower().replace(".", "")
