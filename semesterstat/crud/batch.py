from typing import List

from sqlalchemy.orm import Session, noload

from semesterstat.common.reports import ScoreReport, StudentReport

from ..database import BatchSchemeInfo, Score, Student, Subject


"""
Heirarchy of Batch Crud Operations:


get_batch
    |-> Department Filter   -> List Filters (Optional)
    |-> Semester Filter     -> List Filters (Optional)
    |-> Detained Filter     -> List Filters (Optional)
    |-> BackLog Filter      -> List Filters (Optional)

Purpose:
- Obtain Scores As Per the Given Parameters.

Output:
- List[Student(List[Scores])]

"""


def _get_students_batch(db: Session, batch: int, dept: str = None):
    usns = db.query(Student).filter(Student.Batch == batch).options(noload("Scores"))

    if dept is not None:
        usns = usns.filter(Student.Department == dept)

    return usns


def _get_subjects_sem(db: Session, scheme: int, sem: int = None):
    subcodes = db.query(Subject).filter(Subject.Scheme == scheme)

    if sem is not None:
        subcodes = subcodes.filter(Subject.Semester == sem)

    return subcodes


def get_scheme(db: Session, batch: int) -> str:
    return (
        db.query(BatchSchemeInfo.Scheme).filter(BatchSchemeInfo.Batch == batch).scalar()
    )


def is_batch_exists(db: Session, batch: int):
    sb = db.query(BatchSchemeInfo).filter(BatchSchemeInfo.Batch == batch).exists()

    if db.query(sb).scalar() is False:
        return False

    return True


def get_batch_students(
    db: Session, batch: int, dept: str = None
) -> List[StudentReport]:
    res = _get_students_batch(db, batch, dept)

    return [StudentReport.from_orm(x) for x in res]


def get_batch_students_usn(db: Session, batch: int, dept: str = None) -> List[str]:
    res = _get_students_batch(db, batch, dept).with_entities(Student.Usn)
    return [x.Usn for x in res]


def get_batch_scores(
    db: Session, batch: int, dept: str = None, sem: int = None
) -> List[StudentReport]:
    scheme = get_scheme(db, batch)
    usns = _get_students_batch(db, batch, dept)
    subcodes = _get_subjects_sem(db, scheme, sem)

    scores = (
        db.query(Score)
        .filter(Score.Usn.in_(usns.with_entities(Student.Usn).subquery()))
        .filter(Score.SubjectCode.in_(subcodes.with_entities(Subject.Code).subquery()))
    )

    students = [StudentReport.from_orm(x) for x in usns]
    scores = [ScoreReport.from_orm(x) for x in scores]

    for student in students:
        for score in scores:
            if score.Usn == student.Usn:
                student.Scores.append(score)

    return [student for student in students if len(student.Scores) > 0]


def get_batch_detained_students(db: Session, batch: int, dept: str):
    pass


def get_batch_backlog(db: Session, batch: int, dept: str = None, sem: int = None):
    pass