
positions = {}
""" Positions dict, imported from database ("id", "name", "abbreviation", "attributeX") """
import csv
def loadPositions(path:str) -> csv.DictReader:
    """ Loads the Positions database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            positions[int(row["id"])] = row
        return database
loadPositions("database/persons/Position.csv")
def getPositionId(name:str) -> int:
    """ Returns: Position id by its name / abbreviation """
    for position in positions:
        if name.lower().replace(" ", "").replace("-", "") == positions[position]["name"].lower().replace(" ", "").replace("-", "") or name.upper().replace(" ", "").replace("-", "") == positions[position]["abbreviation"]:
            return int(positions[position]["id"])
    return 1
def getPosition(pos:str) -> dict:
    """ Returns: Position dict by its name / abbreviation """
    return positions[getPositionId(pos)]
def getPositionRate(pos:str, attribute:str) -> float:
    """ Returns: Attribute multiplier of the position name / abbreviation """
    return float(positions[getPositionId(pos)][attribute.lower()+"X"])

