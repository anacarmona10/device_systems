from sqlalchemy.orm import Session

from app.models.device_model import Device


# GET todo
def obtener_todos_los_dispositivos(
    db: Session,
    device_type=None,
    is_available=None,
    brand=None
):

    query = db.query(Device)

    if device_type is not None:
        query = query.filter(
            Device.device_type == device_type
        )

    if is_available is not None:
        query = query.filter(
            Device.is_available == is_available
        )

    if brand is not None:
        query = query.filter(
            Device.brand == brand
        )

    return query.all()


# GET ID
def obtener_dispositivo_por_id(
    db: Session,
    device_id: int
):

    return (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )


# Validar si serial existe
def serial_existe(
    db: Session,
    serial_number: str
):

    dispositivo = (
        db.query(Device)
        .filter(
            Device.serial_number == serial_number
        )
        .first()
    )

    return dispositivo is not None

# Crear un dispositivo
def crear_nuevo_dispositivo(
    db: Session,
    dispositivo
):

    nuevo_dispositivo = Device(
        name=dispositivo.name,
        serial_number=dispositivo.serial_number,
        device_type=dispositivo.device_type,
        brand=dispositivo.brand,
        is_available=dispositivo.is_available
    )

    db.add(nuevo_dispositivo)

    db.commit()

    db.refresh(nuevo_dispositivo)

    return nuevo_dispositivo


# PUT
def actualizar_dispositivo_completo(
    db: Session,
    device_id: int,
    datos
):

    dispositivo = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not dispositivo:
        return None

    dispositivo.name = datos.name
    dispositivo.serial_number = datos.serial_number
    dispositivo.device_type = datos.device_type
    dispositivo.brand = datos.brand
    dispositivo.is_available = datos.is_available

    db.commit()

    db.refresh(dispositivo)

    return dispositivo


# PATCH
def actualizar_dispositivo_parcial(
    db: Session,
    device_id: int,
    datos_actualizacion: dict
):

    dispositivo = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not dispositivo:
        return None

    for campo, valor in datos_actualizacion.items():
        setattr(dispositivo, campo, valor)

    db.commit()

    db.refresh(dispositivo)

    return dispositivo


# DELETE
def eliminar_dispositivo(
    db: Session,
    device_id: int
):

    dispositivo = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not dispositivo:
        return False

    db.delete(dispositivo)

    db.commit()

    return True