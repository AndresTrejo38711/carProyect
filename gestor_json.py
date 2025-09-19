# gestor_json.py

import json

def cargar_datos(ruta):
    try:
        with open(ruta, 'r') as f:
            datos = json.load(f)
            config = datos.get("config", {})
            obst = datos.get("obstaculos", [])
            # Devolver config y lista de dicts con x, y, tipo
            return config, [
                {"x": o["x"], "y": o["y"], "tipo": o.get("tipo", "default")}
                for o in obst
            ]
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, []


