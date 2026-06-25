from fastapi import HTTPException

from app.services.device_service import (
    obtener_dispositivo_por_id,
    serial_existe
)


def get_device_or_404(
    db,
    device_id: int
):

    dispositivo = obtener_dispositivo_por_id(
        db,
        device_id
    )

    if not dispositivo:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return dispositivo


def validar_serial_unico(
    db,
    serial_number: str
):

    if serial_existe(
        db,
        serial_number
    ):

        raise HTTPException(
            status_code=400,
            detail="El número de serie ya está registrado"
        )