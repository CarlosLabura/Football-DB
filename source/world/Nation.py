# id: [subcontinent, continent, abbreviation]
continents = {
    1: ["North America", "America", "NA"],
    2: ["Central America", "America", "CA"],
    3: ["South America", "America", "SA"],
    4: ["Western Europe", "Europe", "WE"],
    5: ["Eastern Europe", "Europe", "EE"],
    6: ["Northern Africa", "Africa", "NAf"],
    7: ["Sub-Saharan Africa", "Africa", "SSA"],
    8: ["Northern Asia", "Asia", "NAs"],
    9: ["Southern Asia", "Asia", "SAs"],
    10: ["Eastern Asia", "Asia", "EAs"],
    11: ["Oceania", "Oceania", "Oc"],
    12: ["Antarctica", "Antarctica", "An"]
}

def getContinentInfo(id:int=1) -> list:
    return continents[int(id)]

nations = {}

import csv
with open("database/world/Nations.csv", mode="r", encoding="utf-8") as archivo:
    lector_csv = csv.DictReader(archivo)

    id = 1
    for fila in lector_csv:
        nations[id] = fila
        id += 1

def getNationInfo(id:int=1) -> dict:
    return nations[int(id)]
