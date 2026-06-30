from fastapi import APIRouter, HTTPException, Query, Response, Depends
from app.schemas.user_schema import UserCreate, UserResponse, RoleEnum
from typing import Optional
from app.services.user_service import (
    obtener_todos_los_usuarios,
    crear_nuevo_usuario,
    actualizar_usuario_completo,
    actualizar_usuario_parcial,
    eliminar_usuario,
    correo_existe
)
from app.schemas.user_schema import UserUpdate


from app.dependencies.user_dependencies import (
    get_user_or_404,
    validar_email_unico
)

router = APIRouter()


from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.dependencies.auth_dependency import (
    require_admin,
    require_support_or_admin
)

from app.models.user_model import User



@router.get("/users", response_model=list[UserResponse])
def listar_usuarios(
    response: Response,
    role: Optional[RoleEnum] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    return obtener_todos_los_usuarios(
        db,
        role,
        is_active,
        sort_by,
        email
    )

# GET /users/{user_id} — por ID
@router.get("/users/{user_id}", response_model=UserResponse)
def obtener_usuario(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_support_or_admin)
):


    return get_user_or_404(
        db,
        user_id
    )


# post
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def crear_usuario(
    usuario: UserCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):


    validar_email_unico(
        db,
        usuario.email
    )

    return crear_nuevo_usuario(
        db,
        usuario
    )


@router.put("/users/{user_id}", response_model=UserResponse)
def actualizar_usuario(
    user_id: int,
    usuario: UserCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):


    get_user_or_404(
        db,
        user_id
    )

    usuario_email = obtener_todos_los_usuarios(db)

    for u in usuario_email:
        if (
            u.email == usuario.email
            and u.id != user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    return actualizar_usuario_completo(
        db,
        user_id,
        usuario
    )



@router.patch("/users/{user_id}", response_model=UserResponse)
def actualizar_usuario_parcialmente(
    user_id: int,
    usuario: UserUpdate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):


    get_user_or_404(
        db,
        user_id
    )

    datos = usuario.model_dump(exclude_unset=True)

    if not datos:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    if "email" in datos:

        usuarios = obtener_todos_los_usuarios(db)

        for u in usuarios:

            if (
                u.email == datos["email"]
                and u.id != user_id
            ):
                raise HTTPException(
                    status_code=400,
                    detail="El correo ya está registrado"
                )

    return actualizar_usuario_parcial(
        db,
        user_id,
        datos
    )


@router.delete("/users/{user_id}")
def eliminar_usuario_endpoint(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):


    get_user_or_404(
        db,
        user_id
    )

    eliminar_usuario(
        db,
        user_id
    )

    return {
        "message": "Usuario eliminado correctamente"
    }