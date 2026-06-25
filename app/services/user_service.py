from app.data.users_db import usuarios_db


def obtener_todos_los_usuarios(role=None, is_active=None):
    resultado = usuarios_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


def obtener_usuario_por_id(user_id:int):

    for usuario in usuarios_db:
        if usuario["id"] == user_id:
            return usuario

    return None


def correo_existe(email:str):

    for usuario in usuarios_db:
        if usuario["email"] == email:
            return True

    return False


def crear_nuevo_usuario(usuario):

    nuevo_id = max(u["id"] for u in usuarios_db) + 1

    nuevo_usuario = {
        "id": nuevo_id,
        **usuario.model_dump()
    }

    usuarios_db.append(nuevo_usuario)

    return nuevo_usuario


def actualizar_usuario_completo(user_id: int, datos):

    for i, usuario in enumerate(usuarios_db):

        if usuario["id"] == user_id:

            usuario_actualizado = {
                "id": user_id,
                **datos.model_dump()
            }

            usuarios_db[i] = usuario_actualizado

            return usuario_actualizado

    return None


def actualizar_usuario_parcial(user_id: int, datos_actualizacion):

    for usuario in usuarios_db:

        if usuario["id"] == user_id:

            usuario.update(datos_actualizacion)

            return usuario

    return None


def eliminar_usuario(user_id: int):

    for i, usuario in enumerate(usuarios_db):

        if usuario["id"] == user_id:

            usuarios_db.pop(i)

            return True

    return False