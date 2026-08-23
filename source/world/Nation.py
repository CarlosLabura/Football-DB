import csv
# TODO:turn this into database
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
""" Continents dict with id ([0]: Subcontinent, [1]: Continent, [2]: Abbreviation) """
def getContinentInfo(id:int=1) -> list:
    """ Gets continent dict content by its id | Returns: Continent dict """
    return continents[int(id)]
nations = {}
""" Nations dict, imported from database ("id", "common_name", "full_name", "abbreviation", "continent_id") """
def loadNations(path:str) -> csv.DictReader:
    """ Loads the Nations database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as archivo:
        file = csv.DictReader(archivo)

        for row in file:
            nations[int(row["id"])] = row
        return file
loadNations("database/world/Nations.csv")
def getNationInfo(id:int=1) -> dict:
    """ Gets nation dict content by its id | Returns: Nation dict """
    return nations[int(id)]
