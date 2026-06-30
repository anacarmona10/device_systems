from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router

from app.database.connection import engine, Base
from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

from app.auth.auth_routes import router as auth_router

from app.middlewares.request_middleware import request_middleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.middlewares.rate_limit import limiter

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0"
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.middleware("http")(request_middleware)

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