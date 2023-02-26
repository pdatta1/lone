from datetime import datetime 
from typing import List 
from pydantic import BaseModel 

class PaymentBaseSchema(BaseModel): 
    
    employee_id: str | None = None 
    amount: float | None = None 


