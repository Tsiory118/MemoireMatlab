from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import csv
from datetime import datetime
import os

# ==================================================
#                FASTAPI + MODELES
# ==================================================

app = FastAPI()

class Measurement(BaseModel):
    distance_mm: int
    angle_deg: float
    height_m: float

class LidarMatrix(BaseModel):
    matrix: List[List[Measurement]]
    timestamp: str


# ==================================================
#              FONCTIONS DE SAUVEGARDE
# ==================================================

def save_to_json(data: dict, filename="data.json"):
    """Ajoute une nouvelle frame dans data.json"""

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as f:
        json.dump(existing_data, f, indent=4)


def save_to_csv(matrix: List[List[Measurement]], timestamp: str, filename="data.csv"):
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        # En-têtes
        if not file_exists:
            header = ["timestamp"] + [f"cell_{i}" for i in range(64)]
            writer.writerow(header)

        row_values = [timestamp]

        for row in matrix:
            for cell in row:
                row_values.append(cell.distance_mm)

        writer.writerow(row_values)


# ==================================================
#                   ENDPOINT API
# ==================================================

@app.post("/lidar")
async def receive_lidar(data: LidarMatrix):

    # --- Vérification 8x8 ---
    while len(data.matrix) < 8:
        data.matrix.append([Measurement(distance_mm=0, angle_deg=0, height_m=0) for _ in range(8)])

    for row in data.matrix:
        while len(row) < 8:
            row.append(Measurement(distance_mm=0, angle_deg=0, height_m=0))

    # --- Extraction uniquement des distances pour MATLAB ---
    distance_matrix = [
        [cell.distance_mm for cell in row]
        for row in data.matrix
    ]

    data_to_save = {
        "timestamp": data.timestamp,
        "distance_mm": distance_matrix
    }

    # Sauvegardes
    save_to_json(data_to_save)
    save_to_csv(data.matrix, data.timestamp)

    return {"status": "ok", "saved": True}
