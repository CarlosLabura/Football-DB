import csv

continents = {}
""" Continents dict, imported from database ("id", "common_name", "full_name", "abbreviation") """
def loadContinents(path:str) -> csv.DictReader:
    """ Loads the Continents database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            continents[int(row["id"])] = row
        return database
loadContinents("database/world/Nations.csv")
def getContinentInfo(id:int=1) -> list:
    """ Gets continent dict content by its id | Returns: Continent dict """
    return continents[int(id)]
nations = {}
""" Nations dict, imported from database ("id", "common_name", "full_name", "abbreviation", "continent_id") """
def loadNations(path:str) -> csv.DictReader:
    """ Loads the Nations database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            nations[int(row["id"])] = row
        return database
loadNations("database/world/Nations.csv")
def getNationInfo(id:int=1) -> dict:
    """ Gets nation dict content by its id | Returns: Nation dict """
    return nations[int(id)]
