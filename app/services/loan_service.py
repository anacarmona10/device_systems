from datetime import datetime

from sqlalchemy.orm import Session

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device

def obtener_prestamos(
    db: Session,
    status=None,
    user_email=None,
    device_type=None
):

    query = (
        db.query(Loan)
        .join(User)
        .join(Device)
    )

    if status is not None:
        query = query.filter(
            Loan.status == status
        )

    if user_email is not None:
        query = query.filter(
            User.email.ilike(f"%{user_email}%")
        )

    if device_type is not None:
        query = query.filter(
            Device.device_type == device_type
        )

    return query.all()


def obtener_prestamo_por_id(
    db: Session,
    loan_id: int
):

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .filter(Loan.id == loan_id)
        .first()
    )

def crear_prestamo(
    db: Session,
    datos
):

    usuario = (
        db.query(User)
        .filter(User.id == datos.user_id)
        .first()
    )

    if not usuario:
        return None


    dispositivo = (
        db.query(Device)
        .filter(Device.id == datos.device_id)
        .first()
    )

    if not dispositivo:
        return False


    if not dispositivo.is_available:
        return "ocupado"


    nuevo_prestamo = Loan(
        user_id=datos.user_id,
        device_id=datos.device_id,
        status=datos.status
    )

    dispositivo.is_available = False

    db.add(nuevo_prestamo)

    db.commit()

    db.refresh(nuevo_prestamo)

    return nuevo_prestamo

def devolver_prestamo(
    db: Session,
    loan_id: int
):

    prestamo = (
        db.query(Loan)
        .filter(Loan.id == loan_id)
        .first()
    )

    if not prestamo:
        return None

    if prestamo.status == "returned":
        return "devuelto"

    dispositivo = (
        db.query(Device)
        .filter(Device.id == prestamo.device_id)
        .first()
    )

    prestamo.status = "returned"
    prestamo.return_date = datetime.utcnow()

    if dispositivo:
        dispositivo.is_available = True

    db.commit()

    db.refresh(prestamo)

    return prestamo


def obtener_prestamos_por_usuario(
    db: Session,
    user_id: int
):

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .filter(Loan.user_id == user_id)
        .all()
    )


def obtener_prestamos_por_dispositivo(
    db: Session,
    device_id: int
):

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .filter(Loan.device_id == device_id)
        .all()
    )