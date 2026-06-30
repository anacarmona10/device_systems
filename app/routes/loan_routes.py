from fastapi import (
    APIRouter,
    Depends,
    Response,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailResponse
)

from app.services.loan_service import (
    crear_prestamo,
    devolver_prestamo,
    obtener_prestamos,
    obtener_prestamo_por_id,
    obtener_prestamos_por_usuario,
    obtener_prestamos_por_dispositivo
)

from app.dependencies.user_dependencies import get_user_or_404

from app.dependencies.device_dependencies import get_device_or_404

from typing import Optional

from app.dependencies.auth_dependency import (
    require_admin,
    require_support_or_admin,
    get_current_user
)

from app.models.user_model import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# GET todos
@router.get(
    "/loans",
    response_model=list[LoanDetailResponse]
)
def listar_prestamos(
    response: Response,

    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,

    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    return obtener_prestamos(
    db,
    status,
    user_email,
    device_type
)


# GET por ID
@router.get(
    "/loans/{loan_id}",
    response_model=LoanDetailResponse
)
def obtener_prestamo(
    loan_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    prestamo = obtener_prestamo_por_id(
        db,
        loan_id
    )

    if not prestamo:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado"
        )

    return prestamo


# GET por user
@router.get(
    "/users/{user_id}/loans",
    response_model=list[LoanDetailResponse]
)
def listar_prestamos_usuario(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    get_user_or_404(
        db,
        user_id
    )

    return obtener_prestamos_por_usuario(
        db,
        user_id
    )


# GET por device
@router.get(
    "/devices/{device_id}/loans",
    response_model=list[LoanDetailResponse]
)
def listar_prestamos_dispositivo(
    device_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    get_device_or_404(
        db,
        device_id
    )

    return obtener_prestamos_por_dispositivo(
        db,
        device_id
    )


# POST (creando ando)
@router.post(
    "/loans",
    response_model=LoanResponse,
    status_code=201
)
def crear(
    datos: LoanCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    return crear_prestamo(
        db,
        datos
    )


# PATCH PATCH
@router.patch(
    "/loans/{loan_id}/return",
    response_model=LoanResponse
)
def devolver(
    loan_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    return devolver_prestamo(
        db,
        loan_id
    )