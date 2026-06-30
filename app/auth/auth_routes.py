from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status
)

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    Token
)

from app.schemas.user_schema import UserResponse

from app.auth.auth_service import (
    registrar_usuario,
    autenticar_usuario,
    generar_token,
    obtener_usuario_por_email
)

from app.dependencies.auth_dependency import get_current_user

from app.models.user_model import User

from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Request

from app.middlewares.rate_limit import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)




# ===========================
# REGISTER
# ===========================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("3/minute")
def register(
    request: Request,
    datos: UserRegister,
    response: Response,
    db: Session = Depends(get_db)
):



    if obtener_usuario_por_email(
        db,
        datos.email
    ):

        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    return registrar_usuario(
        db,
        datos
    )


# ===========================
# LOGIN
# ===========================

@router.post(
    "/login",
    response_model=Token
)
@limiter.limit("5/minute")
def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):



    usuario = autenticar_usuario(
        db,
        form_data.username,
        form_data.password
    )

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    return generar_token(usuario)


# ===========================
# ME
# ===========================

@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user: User = Depends(get_current_user)
):

    return current_user