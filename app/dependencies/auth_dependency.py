from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.auth.security import decode_access_token

from app.models.user_model import User

from app.schemas.user_schema import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    usuario = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return usuario


def require_admin(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != RoleEnum.admin.value:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden realizar esta acción"
        )

    return current_user


def require_support_or_admin(
    current_user: User = Depends(get_current_user)
):

    if current_user.role not in [
        RoleEnum.admin.value,
        RoleEnum.support.value
    ]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos suficientes"
        )

    return current_user