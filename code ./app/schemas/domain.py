from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ==========================================
# BIOMETRIC LOG SCHEMAS (Smart Attendance)
# ==========================================

class BiometricLogBase(BaseModel):
    # Using Field for strict validation constraints
    fatigue_score: float = Field(..., ge=0.0, le=1.0, description="Score from 0.0 (alert) to 1.0 (exhausted)")
    emotion_state: str = Field(..., example="focused")
    access_point: str = Field(..., example="Main Gate Camera A")

class BiometricLogCreate(BiometricLogBase):
    """Schema for data coming IN from the IoT cameras"""
    pass

class BiometricLogResponse(BiometricLogBase):
    """Schema for data going OUT to the frontend dashboard"""
    id: int
    employee_record_id: int
    timestamp: datetime

    # This tells Pydantic to read data directly from the SQLAlchemy database models
    model_config = {"from_attributes": True}


# ==========================================
# EMPLOYEE SCHEMAS (Core HR)
# ==========================================

class EmployeeBase(BaseModel):
    employee_id: str = Field(..., example="EMP-8472")
    full_name: str = Field(..., example="Jane Doe")
    department: str = Field(..., example="Engineering")
    is_active: Optional[bool] = True

class EmployeeCreate(EmployeeBase):
    """Schema for HR creating a new employee"""
    pass

class EmployeeResponse(EmployeeBase):
    """Schema for returning employee data, including their biometric history"""
    id: int
    biometrics: List[BiometricLogResponse] = []

    model_config = {"from_attributes": True}