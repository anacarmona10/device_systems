from fastapi import (
    APIRouter,
    Response,
    Query,
    Depends,
    HTTPException
)

from typing import Optional

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.dependencies.device_dependencies import (
    get_device_or_404,
    validar_serial_unico
)

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
    DeviceTypeEnum
)

from app.services.device_service import (
    obtener_todos_los_dispositivos,
    crear_nuevo_dispositivo,
    actualizar_dispositivo_completo,
    actualizar_dispositivo_parcial,
    eliminar_dispositivo
)

router = APIRouter()

def agregar_cabeceras(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

# GET
@router.get(
    "/devices",
    response_model=list[DeviceResponse]
)
def listar_dispositivos(
    response: Response,
    device_type: Optional[DeviceTypeEnum] = Query(None),
    is_available: Optional[bool] = Query(None),
    brand: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    agregar_cabeceras(response)

    return obtener_todos_los_dispositivos(
        db,
        device_type,
        is_available,
        brand
    )

# GET con ID
@router.get(
    "/devices/{device_id}",
    response_model=DeviceResponse
)
def obtener_dispositivo(
    device_id: int,
    response: Response,
    db: Session = Depends(get_db)
):

    agregar_cabeceras(response)

    return get_device_or_404(
        db,
        device_id
    )

# POST pa crear
@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=201
)
def crear_dispositivo(
    dispositivo: DeviceCreate,
    response: Response,
    db: Session = Depends(get_db)
):

    agregar_cabeceras(response)

    validar_serial_unico(
        db,
        dispositivo.serial_number
    )

    return crear_nuevo_dispositivo(
        db,
        dispositivo
    )

# PUT
@router.put(
    "/devices/{device_id}",
    response_model=DeviceResponse
)
def actualizar_dispositivo_endpoint(
    device_id: int,
    dispositivo: DeviceCreate,
    response: Response,
    db: Session = Depends(get_db)
):

    agregar_cabeceras(response)

    get_device_or_404(
        db,
        device_id
    )

    return actualizar_dispositivo_completo(
        db,
        device_id,
        dispositivo
    )

# PATCH
@router.patch(
    "/devices/{device_id}",
    response_model=DeviceResponse
)
def actualizar_dispositivo_parcial_endpoint(
    device_id: int,
    dispositivo: DeviceUpdate,
    response: Response,
    db: Session = Depends(get_db)
):

    agregar_cabeceras(response)

    get_device_or_404(
        db,
        device_id
    )

    datos = dispositivo.model_dump(
        exclude_unset=True
    )

    if not datos:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    return actualizar_dispositivo_parcial(
        db,
        device_id,
        datos
    )


# DELETE
@router.delete("/devices/{device_id}")
def eliminar_dispositivo_endpoint(
    device_id: int,
    response: Response,
    db: Session = Depends(get_db)
):

    agregar_cabeceras(response)

    get_device_or_404(
        db,
        device_id
    )

    eliminar_dispositivo(
        db,
        device_id
    )

    return {
        "message": "Dispositivo eliminado correctamente"
    }