import source.persons.Position as Position
import source.persons.Player as Player
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
        playerSelected = None
        for i in range(len(self.available)):
            if i == int(player):
                playerSelected = self.available.pop(i)

        if playerSelected == None:
            print("Formation.changePlayer(): No player found")
            return

        self.changed.append(self.players[int(position)])
        self.players[int(position)] = playerSelected