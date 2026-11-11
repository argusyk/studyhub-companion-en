"""Storing uploaded files. The file name has already been validated by the SubmissionCreate schema."""
from pathlib import Path

from app.config import get_settings

UPLOAD_ROOT = Path(get_settings().upload_dir)


def save_upload(lab_id: int, student_id: int, filename: str, data: bytes) -> Path:
    target_dir = UPLOAD_ROOT / str(lab_id) / str(student_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / filename
    # Protection against escaping the directory even if the validation is ever weakened.
    if UPLOAD_ROOT.resolve() not in path.resolve().parents:
        raise ValueError("the path escapes the uploads directory")
    path.write_bytes(data)
    return path
