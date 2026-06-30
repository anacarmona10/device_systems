from fastapi import FastAPI
from app.routes.user_routes import router

from app.database.connection import engine, Base
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

from app.auth.auth_routes import router as auth_router

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST para gestión de usuarios del sistema device_systems",
    version="1.0",
)

app.include_router(auth_router)

app.include_router(router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(
    device_router,
    prefix="/api/v1",
    tags=["Devices"]
)

app.include_router(
    loan_router,
    prefix="/api/v1",
    tags=["Loans"]
)



@app.get("/")
def root():
    return {"message": "Bienvenido a device_systems API", "version": "1.0"}