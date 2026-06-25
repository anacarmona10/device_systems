
from sqlalchemy.orm import Session

from app.models.user_model import User


def obtener_todos_los_usuarios(
    db: Session,
    role=None,
    is_active=None,
    sort_by=None,
    email=None
):

    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if sort_by == "name":
        query = query.order_by(User.name)

    if sort_by == "created_at":
        query = query.order_by(User.created_at)

    elif email is not None:
        query = query.filter(User.email == email)    

    return query.all()

def obtener_usuario_por_id(
    db: Session,
    user_id: int
):

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def correo_existe(
    db: Session,
    email: str
):

    usuario = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    return usuario is not None


def crear_nuevo_usuario(
    db: Session,
    usuario
):

    nuevo_usuario = User(
        name=usuario.name,
        email=usuario.email,
        role=usuario.role,
        is_active=usuario.is_active
    )

    db.add(nuevo_usuario)

    db.commit()

    db.refresh(nuevo_usuario)

    return nuevo_usuario


def actualizar_usuario_completo(
    db: Session,
    user_id: int,
    datos
):

    usuario = obtener_usuario_por_id(
        db,
        user_id
    )

    if not usuario:
        return None

    usuario.name = datos.name
    usuario.email = datos.email
    usuario.role = datos.role
    usuario.is_active = datos.is_active

    db.commit()

    db.refresh(usuario)

    return usuario


def actualizar_usuario_parcial(
    db: Session,
    user_id: int,
    datos_actualizacion: dict
):

    usuario = obtener_usuario_por_id(
        db,
        user_id
    )

    if not usuario:
        return None

    for campo, valor in datos_actualizacion.items():
        setattr(usuario, campo, valor)

    db.commit()

    db.refresh(usuario)

    return usuario


def eliminar_usuario(
    db: Session,
    user_id: int
):

    usuario = obtener_usuario_por_id(
        db,
        user_id
    )

    if not usuario:
        return False

    db.delete(usuario)

    db.commit()

    return True