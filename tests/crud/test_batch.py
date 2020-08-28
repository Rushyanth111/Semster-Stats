from typing import List
from collections import Counter
import pytest
from sqlalchemy.orm.session import Session

from semesterstat.crud import get_batch_students, get_scheme, is_batch_exists
from semesterstat.crud.batch import get_batch_scores, get_batch_students_usn


@pytest.mark.parametrize(
    ["batch", "scheme"], [(2015, 2015), (2016, 2015), (2017, 2017)]
)
def test_get_scheme(db: Session, batch: int, scheme: int):
    res = get_scheme(db, batch)
    assert res == scheme


@pytest.mark.parametrize(["batch", "op"], [(2015, True), (2016, True), (2014, False)])
def test_batch_exists(db: Session, batch: int, op: int):
    assert is_batch_exists(db, batch) == op


@pytest.mark.parametrize(
    ["batch", "dept", "op"],
    [
        (2015, None, ["1CR15CS101", "1CR15CS102"]),
        (2015, "CS", ["1CR15CS101", "1CR15CS102"]),
        (2015, "TE", []),
    ],
)
def test_batch_students(db: Session, batch: int, dept: str, op: List[str]):
    res = get_batch_students(db, batch, dept)
    assert [x.Usn for x in res] == op


@pytest.mark.parametrize(
    ["batch", "dept", "op"],
    [
        (2015, None, ["1CR15CS101", "1CR15CS102"]),
        (2015, "CS", ["1CR15CS101", "1CR15CS102"]),
        (2015, "TE", []),
    ],
)
def test_batch_students_usn(db: Session, batch: int, dept: str, op: List[str]):
    assert get_batch_students_usn(db, batch, dept) == op


@pytest.mark.parametrize(
    ["batch", "dept", "sem", "opusn", "opsubcode"],
    [
        (
            2015,
            None,
            None,
            ["1CR15CS101", "1CR15CS102"],
            ["15CS65", "15CS64", "15CS54"],
        ),
        (2014, None, None, [], []),
        (2015, "CS", 6, ["1CR15CS101"], ["15CS65", "15CS64"]),
    ],
)
def test_batch_scores(
    db: Session, batch: int, dept: str, sem: int, opusn: List[str], opsubcode: List[str]
):
    res = get_batch_scores(db, batch, dept, sem)

    assert Counter(opusn) == Counter([x.Usn for x in res])
    assert Counter(opsubcode) == Counter([y.SubjectCode for x in res for y in x.Scores])