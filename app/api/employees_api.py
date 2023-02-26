
from app.database import get_db
from app.models import Employee
from app.schemas.employee import EmployeeBaseSchema
from fastapi import Depends, HTTPException, status, APIRouter, Response

from sqlalchemy.orm import Session


employee_router = APIRouter() 


@employee_router.get('/', status_code=status.HTTP_200_OK)
def get_employees(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''): 
    
    skip = (page - 1) * limit 

    employees = db.query(Employee).filter(Employee.first_name.contains(search)).limit(limit).offset(skip).all()
    return { 
        "status": status.HTTP_200_OK,
        "results": len(employees),
        "employees": employees,
    }


@employee_router.post('/', status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeBaseSchema, db: Session = Depends(get_db)): 

    employee = Employee(**payload.dict()) 
    db.add(employee)
    db.commit() 
    db.refresh(employee)

    return {
        "status": status.HTTP_201_CREATED,
        "employee_created": employee,
    }


@employee_router.patch('/{employeeId}')
def update_employee(employeeId: str, payload: EmployeeBaseSchema, db: Session = Depends(get_db)): 
    
    employee_query = db.query(Employee).filter(Employee.id == employeeId)
    employee_data = employee_query.first() 

    if not employee_data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id not found: (ID : {employeeId})")
    
    update_data = payload.dict(exclude_unset=True)
    employee_query.filter(Employee.id == employeeId).update(update_data, synchronize_session=False)

    db.commit() 
    db.refresh(employee_data)

    return { "status": status.HTTP_200_OK, "updated_data": employee_data}



@employee_router.get('/{employeeId}')
def get_employee_by_id(employeeId: str, db: Session = Depends(get_db)): 

    employee_data = db.query(Employee).filter(Employee.id == employeeId).first() 

    if not employee_data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error find employee with id: {employeeId}")
    
    return { 
        "status": status.HTTP_200_OK,
        "employee": employee_data
    }


@employee_router.get('/{employeeId}')
def delete_employee_by_id(employeeId: str, db: Session = Depends(get_db)): 

    employee_data = db.query(Employee).filter(Employee.id == employeeId).first() 

    if not employee_data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error delete employee, cannot find given id: {employeeId}")
    
    employee_data.delete(synchronize_session=False)

    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


