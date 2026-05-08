from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation = Column(String, nullable=False)
    phone = Column(String, nullable=True)