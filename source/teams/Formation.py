import source.persons.Position as Position
from source.persons.Player import Player
import csv

formations = {}

def loadFormations(path:str):
    with open(path, mode="r", encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(archivo)

        for fila in lector_csv:
            formations[int(fila["id"])] = fila

loadFormations("database/teams/Formations.csv")

class Formation:
    def __init__(self, formation:int, players:set):
        self.formation = formations[int(formation)]
        self.available = set(players)
        self.players = {}
        self.changed = set()

    def changePlayer(self, position:int, player:int):
        self.available.remove(int(player))
        self.players[int(position)] = int(player)
        self.changed.add(self.players[int(position)])

    def getPosition(self, id:int):
        return Position.positions[int(self.formation["pos"+str(id)])]
    def getPlayer(self, id:int):
        return Player.get(self.players[int(id)])
    def getPlayerOverall(self,id:int):
        return self.getPlayer(id).getOverall(self.getPosition(id)["name"])