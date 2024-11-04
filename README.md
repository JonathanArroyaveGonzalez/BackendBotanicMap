# Proyecto BotanicMap


## Arquitectura MVC

El proyecto sigue el patrón de arquitectura Modelo-Vista-Controlador (MVC):

- **Modelos (Models)**: Definidos en el archivo [app/models.py](app/models.py). Aquí se definen las clases que representan las tablas de la base de datos.
- **Vistas (Views)**: En este caso, las vistas son los endpoints definidos en los routers. Los routers están ubicados en la carpeta [app/routers](app/routers).
- **Controladores (Controllers)**: La lógica de negocio y las operaciones CRUD están definidas en el archivo [app/crud.py](app/crud.py).

## Deploy
[Backend BotanicMap](https://backendbotanicmap.onrender.com/docs)

## Endpoints

### Fauna

- **GET /fauna/getAllFauna**: Obtiene una lista de todas las faunas.
- **GET /fauna/getFaunaById/{fauna_id}**: Obtiene una fauna por su ID.
- **POST /fauna/createFauna**: Crea una nueva fauna.
- **DELETE /fauna/deleteFaunaById/{fauna_id}**: Elimina una fauna por su ID.

### Flora

- **GET /flora/getAllFlora**: Obtiene una lista de todas las floras.
- **GET /flora/getFloraById/{flora_id}**: Obtiene una flora por su ID.
- **POST /flora/flora/**: Crea una nueva flora.
- **DELETE /flora/flora/{flora_id}**: Elimina una flora por su ID.

### Puntos de Interés (POI)

- **GET /pio/getAllPois**: Obtiene una lista de todos los puntos de interés.
- **GET /pio/getPoiById/{poi_id}**: Obtiene un punto de interés por su ID.
- **POST /pio/createPois**: Crea un nuevo punto de interés.
- **DELETE /pio/deletePoisById/{poi_id}**: Elimina un punto de interés por su ID.

### Health Check

- **GET /healthCheck**: Verifica que la aplicación esté funcionando correctamente.

## Comandos para ejecutar el proyecto

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:
    ```sh
    uvicorn app.main:app --reload
    ```

4. Accede a la documentación interactiva de la API en:
    ```
    http://127.0.0.1:8000/docs
    ```

## Descripción de Archivos

- **app/crud.py**: Contiene las funciones CRUD para interactuar con la base de datos.
- **app/database.py**: Configuración de la base de datos.
- **app/main.py**: Punto de entrada de la aplicación.
- **app/models.py**: Definición de los modelos de la base de datos.
- **app/routers/**: Contiene los routers para los diferentes endpoints.
- **app/schemas.py**: Definición de los esquemas Pydantic para la validación de datos.

