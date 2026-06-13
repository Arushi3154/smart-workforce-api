from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    department = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Establish a one-to-many relationship with biometric logs
    biometrics = relationship("BiometricLog", back_populates="employee")


class BiometricLog(Base):
    __tablename__ = "biometric_logs"

    id = Column(Integer, primary_key=True, index=True)
    employee_record_id = Column(Integer, ForeignKey("employees.id"))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # IoT & Machine Learning Data Points
    fatigue_score = Column(Float)  # e.g., 0.0 to 1.0 based on eye aspect ratio
    emotion_state = Column(String) # e.g., focused, stressed, neutral
    access_point = Column(String)  # Location of the camera/sensor
    
    employee = relationship("Employee", back_populates="biometrics")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="admin")  # e.g., admin, hr, gate_node