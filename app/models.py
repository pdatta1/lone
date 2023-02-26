
import uuid 

from typing import List 
from typing import Optional

from sqlalchemy import String, Integer, ForeignKey, Column, TIMESTAMP, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func 



Base = declarative_base() 


class Employee(Base): 

    __tablename__ = "employees"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    position = Column(String(50), nullable=False)
    date_started = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    salary = Column(Float, nullable=False)

    payments = relationship("Payment", back_populates="employee", cascade="all, delete-orphan")


    def __repr__(self): 
        return f"User(id={self.id}, FirstName={self.first_name}, LastName={self.last_name}, Position={self.position})"
    


class Payment(Base): 

    __tablename__ = "payments"


    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    employee_id = Column(String, ForeignKey("employees.id"), nullable=False)

    amount = Column(Float, nullable=False)
    payment_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    employee = relationship("Employee", back_populates="payments")

    def __repr__(self): 
        return f"Payment(id={self.id}, employee_id={self.employee_id}, date={self.payment_date}, amout={self.amount})"