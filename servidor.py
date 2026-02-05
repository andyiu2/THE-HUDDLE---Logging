from flask import Flask, request, jsonify
from datetime import datetime
from database import init_db, insert_logs
import sqlite3

# creamos la aplicacion Flask
app = Flask(__name__)

# definimos el token de cada servicio
TOKENS = {
    "token_a" : "servicio01",
    "token_b" : "servicio02"
}

# esta funcion extrae el token del header solo si cumple con el formato "Token {token}"
def obtener_servicio_con_token():
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Token "):
        return None
    
    token = auth.replace("Token ", "")
    return TOKENS.get(token)


# decorador que vincula una ruta a la aplicacion y ejecuta la funcion recibir logs cuando el cliente ingrese a la ruta vinculada y utilice el metodo POST
@app.route("/logs", methods=["POST"])
def recibir_logs():
    servicio = obtener_servicio_con_token()
    if not servicio:
        return jsonify({"error" : "no identificado"}), 401
    
    logs = request.get_json()

    # isinstance verifica que lo que recibe el servidor sea una lista porque el cliente envia varios logs a la vez
    if not isinstance(logs, list):
        return jsonify({"error" : "Se esperaba una lista de logs"}), 400
    
    now = datetime.utcnow().isoformat()

    # construimos el diccionario con los datos del log para devolverlo como JSON y guardarlo en la base de datos
    for log in logs:
        log_data = {
            "timestamp" : log["timestamp"],
            "received_at" : now,
            "service" : servicio, 
            "severity" : log["severity"],
            "message" : log["message"]
        }

        insert_logs(log_data)

    return jsonify({"message" : "Logs guardados correctamente"}), 201

# funcion que se ejecuta cuando el cliente utiliza el metodo GET para realizar consultas con filtros 
@app.route("/logs", methods=["GET"])
def get_logs():
    query = "SELECT timestamp, received_at, service, severity, message FROM logs WHERE 1=1"
    params = []

    ts_start = request.args.get("timestamp_start")
    ts_end = request.args.get("timestamp_end")
    ra_start = request.args.get("received_at_start")
    ra_end = request.args.get("received_at_end")

    if ts_start:
        query += " AND timestamp >= ?"
        params.append(ts_start)
    if ts_end:
        query += " AND timestamp <= ?"
        params.append(ts_end)
    if ra_start:
        query += " AND received_at >= ?"
        params.append(ra_start)
    if ra_end:
        query += " AND received_at <= ?"
        params.append(ra_end)

    query += " ORDER BY received_at DESC"

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    logs = [
        {
            "timestamp": r[0],
            "received_at": r[1],
            "service": r[2],
            "severity": r[3],
            "message": r[4]
        }
        for r in rows
    ]

    return jsonify(logs), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)