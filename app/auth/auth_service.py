from sqlalchemy.orm import Session

from app.models.user_model import User

from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token
)


def obtener_usuario_por_email(
    db: Session,
    email: str
):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def registrar_usuario(
    db: Session,
    datos
):

    usuario = User(
        name=datos.name,
        email=datos.email,
        hashed_password=get_password_hash(
            datos.password
        ),
        role=datos.role,
        is_active=True
    )

    db.add(usuario)

    db.commit()

    db.refresh(usuario)

    return usuario


def autenticar_usuario(
    db: Session,
    email: str,
    password: str
):

    usuario = obtener_usuario_por_email(
        db,
        email
    )

    if not usuario:
        return None

    if not verify_password(
        password,
        usuario.hashed_password
    ):
        return None

    return usuario


def generar_token(usuario):

    access_token = create_access_token(
        {
            "sub": usuario.email,
            "role": usuario.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }