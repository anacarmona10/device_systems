# device_systems

API REST construida con FastAPI para la gestión de usuarios.

## Explicación de la estructura

El proyecto fue organizado siguiendo una estructura modular con el fin de repartir responsabiliddaes y facilitar el mantenimiento del proyecto. La carpeta routes contiene los endpoinys de la API y la definición de las rutas disponibles para el recurso usuarios. La carpeta schemas almacena los modelos Pydantic utilizados para validar los datos de entrad y salida. En services se implementó la lógica de negocio relacionada con la gestión de usuarios, como consultas, creación, actualización y eliminación. La carpeta dependencies contiene funciones reutilizables utilizadas mediante Dependeny Injection para validar información y controlar errores. Finalmente, la carpeta data simula una base de datos en memoria donde se almacenan temporalmente los registros de usuarios. Esta organizaxión permite mantener el código más limpio, escalable y fácil de mantener.

## Explicación de cómo se aplicó Dependency Injection

Se implementó utilizando la función Depends() de FastApI. Para ello se creó el archivo user_dependencies.py, donde se definieron funciones reutilizables como get_user_or_404, encargada de buscar un usuario por su ID y generar una exepción cuando el usuario no existe.

## Evidencias
### Interfaz general
 ![Interfaz](img/Interfaz.png)

 ### Obtener lista de usuarios
 ![ObtenerTodos](img/ObtenerTodos.png)

### Obtener por ID
 ![ObtenerPorID](img/ObtenerID.png)

### Filtrar por rol
![FiltrarRol](img/FiltrarRol.png)

### Crear usuario
![CrearUsuario](img/CrearUsuario.png)

### Crear usuario (Datos incorrectos)
![Error 422](img/Error422.png)

### Correo repetido
![CorreoRepetido](img/Error400.png)

### No encontrado
![Error404](img/Error404.png)

## Reflexión final sobre la evolución del proyecto

Durante el desarrollo de esta actividad fue posible comprender cómo una API REST puede evolucionar desde una implementación básica hacia una solución más profesional y estructurada.