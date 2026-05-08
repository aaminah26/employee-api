from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.department import Department
from schemas.department import DepartmentCreate

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


@router.post("/")
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    new_department = Department(
        name=department.name,
        location=department.location
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


@router.put("/{id}")
def update_department(
    id: int,
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    dept = db.query(Department).filter(
        Department.id == id
    ).first()

    if not dept:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    dept.name = department.name
    dept.location = department.location

    db.commit()

    return {"message": "Department updated"}


@router.delete("/{id}")
def delete_department(
    id: int,
    db: Session = Depends(get_db)
):

    dept = db.query(Department).filter(
        Department.id == id
    ).first()

    if not dept:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(dept)
    db.commit()

    return {"message": "Department deleted"}