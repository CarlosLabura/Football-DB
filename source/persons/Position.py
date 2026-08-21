
positions = {}

import csv
with open("database/persons/position.csv", mode="r", encoding="utf-8") as archivo:
    lector_csv = csv.DictReader(archivo)

    for fila in lector_csv:
        positions[int(fila["id"])] = fila

def getPositionId(name:str) -> int:
    for position in positions:
        if name.lower().replace(" ", "").replace("-", "") == positions[position]["name"].lower().replace(" ", "").replace("-", "") or name.upper().replace(" ", "").replace("-", "") == positions[position]["abbreviation"]:
            return int(positions[position]["id"])
    return 1

def getPosition(pos:str):
    return positions[getPositionId(pos)]

def getPositionRate(pos:str, typ:str) -> float:
    return float(positions[getPositionId(pos)][typ.lower()+"X"])
    
