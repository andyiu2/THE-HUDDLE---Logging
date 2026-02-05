import requests
import time 
from datetime import datetime
import random

# ruta para acceder al servidor
URL = "http://127.0.0.1:5000/logs"


SERVICES = [
    {"token" : "token_a"},
    {"token" : "token_b"}
]

SEVERITIES = ["INFO", "DEBUG", "ERROR"]

# ciclo para simulacion de trafico de logs
while True:
    for service in SERVICES:
        logs = []

        # se envian 2 logs en cada ciclo
        for _ in range(2):
            logs.append({
                "timestamp" : datetime.utcnow().isoformat(),
                "severity" : random.choice(SEVERITIES),
                "message" : "Evento simulado del sistema"
            })

        headers = {
            "Authorization" : f"Token {service['token']}"
        }

        requests.post(URL, json=logs, headers=headers)
    time.sleep(2)