
from app.database import get_db
from app.models import Payment
from app.models import Employee

from app.schemas.payments import PaymentBaseSchema

from fastapi import APIRouter, Response, status, Depends, HTTPException

from sqlalchemy.orm import Session 


payment_router = APIRouter() 


@payment_router.get('/', status_code=status.HTTP_200_OK)
def get_payments(db: Session = Depends(get_db), limit: int = 20, page: int = 1, search: str = ''): 

    skip = (page - 1) * limit 

    payments = db.query(Payment).filter(Payment.id.contains(search)).limit(limit).offset(skip).all() 
    return { 
        "status": status.HTTP_200_OK, 
        "results": len(payments),
        "payments": payments 
    }


@payment_router.post('/', status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentBaseSchema, db: Session = Depends(get_db)): 

    payment = Payment(**payload.dict())
    try: 
        db.add(payment)
        db.commit() 
        db.refresh(payment)
    except: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating payment!")
    
    finally: 
        return { 
            "status": status.HTTP_201_CREATED, 
            "payment": payment 
        }


@payment_router.get('/employee_payments_lookup', status_code=status.HTTP_200_OK)
def get_employee_payments(db: Session = Depends(get_db), limit: int = 20, page: int = 1, search: str = ''): 

    if search is None: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error with search lookup : {search}")
    
    employee = db.query(Employee).filter(Employee.id.contains(search)).first() 
    
    if not employee: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot find Employee with ID: {search}")
    
    skip = (page - 1) * limit 
    payment_query = db.query(Payment).filter(Payment.employee_id.contains(employee.id)).limit(limit).offset(skip).all() 

    return { 
        "status": status.HTTP_200_OK, 
        "result": len(payment_query),
        "payments": payment_query,
        "employee": employee  
    }