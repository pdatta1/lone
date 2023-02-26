
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import Base 
from app.database import engine 
from app.api.employees_api import employee_router
from app.api.payments_api import payment_router 

Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = [ 
    "http://localhost:3000"
]

#middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)


# routers 
app.include_router(employee_router, tags=["Employee"], prefix='/api/employee')
app.include_router(payment_router, tags=["Payments"], prefix='/api/payments')


@app.get('/healthchecker')
def root(): 
    return { 
        "message": "Lone App is working fine"
    }


