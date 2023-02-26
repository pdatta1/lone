
from datetime import datetime
from typing import List 

from pydantic import BaseModel



class EmployeeBaseSchema(BaseModel): 

    first_name: str | None = None 
    last_name: str | None = None 
    position: str | None = None 
    date_started: datetime | None = None 
    salary: float | None = None 
    payments: List | None = None 


    class Config: 
        orm_mode = True 
        allow_population_by_field_name = True 
        arbitrary_type_allowed = True 






class EmployeeBaseResponse(BaseModel): 

    status: str 
    results: int 
    employees: List[EmployeeBaseSchema]

