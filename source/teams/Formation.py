import source.persons.Position as Position
from source.persons.Player import Player
import csv

formations = {}
""" Formations dict, imported from database ("id", "formation", "style", "pos1", "pos1x", etc) """
def loadFormations(path:str) -> csv.DictReader:
    """ Loads the Formations database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as archivo:
        file = csv.DictReader(archivo)

        for row in file:
            formations[int(row["id"])] = row
        return file
loadFormations("database/teams/Formations.csv")
class Formation:
    def __init__(self, formation:int, players:set) -> Formation:
        """ Starts a Formation object | Returns: self """
        self.formation = formations[int(formation)]
        """ Formation data from formations dict """
        self.available = set(players)
        """ Players (id) available for changing into formation """
        self.changed = set()
        """ Players (id) changed from formation with changePlayer() """
        self.players = {}
        """ Players (id) in current formation, stored by their position IN FORMATION (1-11) (self.players[10] = 21) """
    def changePlayer(self, position:int, player:int):
        """ Change player (id) selected for the position IN FORMATION (1-11) selected """
        self.available.remove(int(player))
        self.players[int(position)] = int(player)
        self.changed.add(self.players[int(position)])
    def getPosition(self, id:int) -> dict:
        """ Get Position dict from the position IN FORMATION (1-11) | Returns: Position dict """
        return Position.positions[int(self.formation["pos"+str(id)])]
    def getPlayer(self, id:int) -> Player:
        """ Get Player object from the position IN FORMATION (1-11) | Returns: Player object """
        return Player.get(self.players[int(id)])
    def getPlayerOverall(self,id:int) -> int:
        """ Get Player overall for the position IN FORMATION (1-11) they are playing | Returns: Player overall int """
        return self.getPlayer(id).getOverall(self.getPosition(id)["name"])