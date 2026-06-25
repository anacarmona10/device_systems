from fastapi import HTTPException
from app.services.user_service import (
    obtener_usuario_por_id,
    correo_existe
)


def get_user_or_404(user_id:int):

    usuario = obtener_usuario_por_id(user_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


def validar_email_unico(email:str):

    if correo_existe(email):

        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )