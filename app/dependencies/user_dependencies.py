from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.user_service import (
    obtener_usuario_por_id,
    correo_existe
)


def get_user_or_404(
    db: Session,
    user_id: int
):

    usuario = obtener_usuario_por_id(
        db,
        user_id
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


def validar_email_unico(
    db: Session,
    email: str
):

    if correo_existe(
        db,
        email
    ):

        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )