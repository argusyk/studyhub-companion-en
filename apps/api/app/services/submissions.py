from datetime import datetime

from sqlalchemy.orm import Session

from app import storage
from app.clock import server_now_naive
from app.models import Lab, Student, Submission
from app.schemas.submission import SubmissionCreate


class NotFound(Exception):
    """The lab or the student does not exist."""


def mark_submission(submission: Submission, lab: Lab, at_utc: datetime | None = None) -> None:
    """Marks a submission as late if it is after the deadline."""
    submitted = server_now_naive(at_utc)
    deadline = lab.deadline.replace(tzinfo=None)  # we compare the columns "as is"
    submission.is_late = submitted > deadline


def create_submission(db: Session, lab_id: int, payload: SubmissionCreate, data: bytes) -> Submission:
    lab = db.get(Lab, lab_id)
    if lab is None:
        raise NotFound(f"lab {lab_id}")
    if db.get(Student, payload.student_id) is None:
        raise NotFound(f"student {payload.student_id}")
    path = storage.save_upload(lab_id, payload.student_id, payload.filename, data)
    sub = Submission(
        lab_id=lab_id,
        student_id=payload.student_id,
        file_url=path.as_posix(),
        filename=payload.filename,
        size_bytes=len(data),
    )
    mark_submission(sub, lab)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub
