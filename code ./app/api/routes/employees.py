from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import domain as models
from app.schemas import domain as schemas
from app.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/employees", tags=["Employees & Biometrics"])

@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(
    employee: schemas.EmployeeCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    db_emp = db.query(models.Employee).filter(models.Employee.employee_id == employee.employee_id).first()
    if db_emp:
        raise HTTPException(status_code=400, detail="Employee ID already registered")
    
    new_emp = models.Employee(**employee.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@router.post("/{employee_id}/biometrics", response_model=schemas.BiometricLogResponse)
def log_biometric(
    employee_id: int, 
    log: schemas.BiometricLogCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    db_emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    new_log = models.BiometricLog(**log.model_dump(), employee_record_id=employee_id)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def get_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    db_emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_emp