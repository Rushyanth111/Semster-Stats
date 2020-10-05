from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..crud.student import (
    get_student,
    get_student_backlogs,
    get_student_scores,
    get_student_subject,
    is_student_exists,
    put_student,
    update_student,
)
from ..crud.subject import is_subject_exist
from ..database import get_db
from ..reciepts import ScoreReciept, StudentScoreReciept
from ..reports import StudentReport

student = APIRouter()


def common_student_verify(usn: str, db: Session = Depends(get_db)) -> str:
    if not is_student_exists(db, usn):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student Not found!"
        )
    return usn


@student.get(
    "/{usn}",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": ["1CX15CX001", "1CX15CX002", "1CX15CX003"],
                    "schema": {
                        "title": "DeptListReciept",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                }
            }
        },
        404: {"description": "Resources Not Found."},
    },
)
def student_get(
    usn: str = Depends(common_student_verify), db: Session = Depends(get_db)
):
    return get_student(db, usn)


@student.get("/{usn}/{semester}", response_model=StudentScoreReciept)
def student_get_semester_scores(
    sem: int, usn: str = Depends(common_student_verify), db: Session = Depends(get_db)
):
    return get_student_scores(db, usn, sem)


@student.get("/{usn}/backlogs", response_model=StudentScoreReciept)
def student_get_backlog(
    sem: int, usn: str = Depends(common_student_verify), db: Session = Depends(get_db)
):
    return get_student_backlogs(db, usn, sem)


@student.get("/{usn}/subject/{subcode}", response_model=ScoreReciept)
def student_get_subject_score(
    subcode: str,
    usn: str = Depends(common_student_verify),
    db: Session = Depends(get_db),
):
    if not is_subject_exist(subcode):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject Not Found."
        )
    return get_student_subject(db, usn, subcode)


@student.post("/")
def student_insert(obj: StudentReport, db: Session = Depends(get_db)):
    put_student(db, obj)


@student.put("/{usn}")
def student_update(
    obj: StudentReport,
    usn: str = Depends(common_student_verify),
    db: Session = Depends(get_db),
):
    update_student(db, usn, obj)
