from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.employee import Employee
from models.user import User
from schemas.employee import EmployeeCreate
from dependencies import get_current_user

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL EMPLOYEES
@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


# CREATE EMPLOYEE
@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department_id=employee.department_id,
        designation=employee.designation,
        phone=employee.phone
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee created successfully",
        "employee": new_employee
    }


# UPDATE EMPLOYEE
@router.put("/{id}")
def update_employee(
    id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    emp = db.query(Employee).filter(Employee.id == id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp.name = employee.name
    emp.email = employee.email
    emp.department_id = employee.department_id
    emp.designation = employee.designation
    emp.phone = employee.phone

    db.commit()
    db.refresh(emp)

    return {
        "message": "Employee updated successfully",
        "employee": emp
    }


# DELETE EMPLOYEE
@router.delete("/{id}")
def delete_employee(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    emp = db.query(Employee).filter(Employee.id == id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(emp)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }