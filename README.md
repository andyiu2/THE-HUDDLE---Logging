<Div align= center>
  <img width="400" height="300" alt="image" src="https://camo.githubusercontent.com/884a213c0c6b6d94db3d3923607eda9f00fe28db86a03f5acb4c0ed83dfe4d95/68747470733a2f2f696d672e6574696d672e636f6d2f7468756d622f6d7369642d38343134363038332c77696474682d313031352c6865696768742d3736312c696d6773697a652d3633383035332c726573697a656d6f64652d382c7175616c6974792d3130302f7072696d652f746563686e6f6c6f67792d616e642d73746172747570732f626f6f74696e672d75702d646576656c6f7065722d65636f6e6f6d792d686f772d746563682d73746172747570732d6172652d68656c70696e672d636f646572732d6275696c642d616e642d746573742d736f6674776172652d6661737465722e6a7067" />

</Div>

🛡️ Centralized Log API (Flask)
===============================

Este proyecto es una **API REST** diseñada para centralizar logs (registros de eventos) provenientes de múltiples servicios. Permite recibir ráfagas de logs de forma segura mediante autenticación por token, almacenarlos en una base de datos y realizar consultas filtradas por tiempo de envío o recepción.

✨ Características Principales
-----------------------------

-   **Autenticación mediante Tokens:** Solo servicios autorizados pueden enviar logs utilizando el encabezado `Authorization: Token {tu_token}`.

-   **Ingesta Masiva:** Capacidad para procesar listas de objetos JSON en una sola petición.

-   **Timestamp Dual:** Registra tanto el momento en que ocurrió el evento en el cliente (`timestamp`) como el momento en que llegó al servidor (`received_at`).

-   **Endpoint de Consulta Flexible:** Búsqueda y filtrado de logs mediante parámetros de consulta (Query Params) para análisis temporal.

* * * * *

🛠️ Stack Tecnológico
---------------------

-   **Backend:** Python con **Flask**.

-   **Base de Datos:** SQLite3 para almacenamiento ligero y persistente.

-   **Formato de Intercambio:** JSON.

* * * * *

🛰️ Endpoints de la API
-----------------------

### 1\. Enviar Logs (POST)

**Ruta:** `/logs` **Headers:** `Authorization: Token <token_a|token_b>`

**Cuerpo (JSON):**

JSON

```
[
  {
    "timestamp": "2024-05-20T10:00:00",
    "severity": "INFO",
    "message": "Inicio de sesión exitoso"
  },
  {
    "timestamp": "2024-05-20T10:01:05",
    "severity": "ERROR",
    "message": "Fallo de conexión a BD"
  }
]

```

### 2\. Consultar Logs (GET)

**Ruta:** `/logs` **Parámetros opcionales:**

-   `timestamp_start` / `timestamp_end`: Filtra por la fecha del evento.

-   `received_at_start` / `received_at_end`: Filtra por la fecha de llegada al servidor.

**Ejemplo de consulta:** `GET /logs?severity=ERROR&received_at_start=2024-05-20T00:00:00`

* * * * *

🗄️ Estructura del Proyecto
---------------------------

-   `server.py`: El núcleo de la API (Flask), manejo de rutas y lógica de autenticación.

-   `database.py`: (Importado) Contiene la lógica para inicializar la tabla y las inserciones SQL.

-   `cliente.py`: (Externo) Script que simula un servicio enviando datos al servidor.

* * * * *

🚀 Cómo empezar
---------------

1.  **Instalar Flask:**

    Bash

    ```
    pip install flask

    ```

2.  **Iniciar el servidor:**

    Bash

    ```
    python server.py

    ```

    *El servidor se ejecutará en `http://127.0.0.1:5000` e inicializará automáticamente `logs.db`.*

* * * * *

🔒 Seguridad Implementada
-------------------------

La función `obtener_servicio_con_token()` actúa como un middleware sencillo, validando que el token enviado en los headers coincida con los servicios registrados (`servicio01` o `servicio02`), devolviendo un error **401 Unauthorized** si el token es inválido o no existe.
