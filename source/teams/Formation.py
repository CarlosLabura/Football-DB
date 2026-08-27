import source.persons.Position as Position
from source.persons.Player import Player
import csv
import math

formations = {}
""" Formations dict, imported from database ("id", "formation", "style", "pos1-11", "pos1-11x", etc) """
def loadFormations(path:str) -> csv.DictReader:
    """ Loads the Formations database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            formations[int(row["id"])] = row
        return database
loadFormations("database/teams/Formations.csv")
class Formation:
    def __init__(self, formation:int, players:set) -> Formation:
        """ Starts a Formation object | Returns: self """
        self.formation:dict = formations[int(formation)]
        """ Formation data from formations dict """
        self.available = set(players)
        """ Players (id) available for changing into formation """
        self.team = set(players)
        self.changed = []
        """ Players (id) changed from formation with changePlayer() [Player (id) who entered, Player (id) who left]"""
        self.players = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
        }
        """ Players (id) in current formation, stored by their position IN FORMATION (1-11) (self.players[10] = 21) """
        self.starter = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
        }
    def __str__(self):
        """ Returns: Formation object into a readable string """
        string = ""
        for i in range(1,12):
            string = string + self.getPosition(i)["abbreviation"] + ": " + self.getPlayer(i).getName() + "\n"

        return string
    def reset(self):
        """ Reset formation """
        self.players = self.starter
        self.changed = []
        self.available = self.team
    def changePlayer(self, position:int, player:int, starter:bool = False):
        """ Change player (id) selected for the position IN FORMATION (1-11) selected | Returns: Player object changed or None """
        position = max(1, min(11, int(position)))

        plrChanged = self.players[int(position)]
        if plrChanged != None:
            plrChanged = Player.get(plrChanged)

        self.available.remove(int(player))
        self.players[int(position)] = int(player)
        if starter:
            self.starter[int(position)] = int(player)
        else:
            self.changed.append([player, plrChanged.id])
        return plrChanged
    def getPlayerList(self) -> list:
        """ Returns: Player id list in formation """
        playerList = []

        for player in self.players:
            playerList.append(player+1)

        return playerList
    def getPosition(self, id:int) -> dict:
        """ Get Position dict from the position IN FORMATION (1-11) | Returns: Position dict """
        id = max(1, min(11, int(id)))
        return Position.positions[int(self.formation["pos"+str(id)])]
    def getPlayer(self, id:int) -> Player:
        """ Get Player object from the position IN FORMATION (1-11) | Returns: Player object """
        id = max(1, min(11, int(id)))
        return Player.get(self.players[int(id)])
    def getPlayerOverall(self,id:int) -> int:
        """ Get Player overall for the position IN FORMATION (1-11) they are playing | Returns: Player overall int """
        id = max(1, min(11, int(id)))
        return self.getPlayer(id).getPositionOverall(self.getPosition(id)["name"])
    def getMultipliers(self, id:int) -> list:
        """ Gets Defense, Passing, Attacking multiplier for the position IN FORMATION (1-11) | Returns: List with the multipliers in order [0, 0.5, 1] """
        id = max(1, min(11, int(id)))
        return list(map(float, self.formation["pos" + str(id) + "x"].split("|")))
    def getPoints(self, section:int) -> list:
        """ Gets a list with the points each section of the team has (1: Defense, 2: Passing, 3: Attacking) | Returns: List with points in sections """
        section = max(1, min(3, int(section)))
        teamMults = []
        for i in range(2,12):
            teamMults.append(math.ceil(self.getPlayerOverall(i) * self.getMultipliers(i)[section-1] * self.getPlayer(i).energy))

        return math.ceil(sum(teamMults))
    def getTeamPoints(self, section:int) -> list:
        """ Gets a list with the points each section of the team has (1: Defense, 2: Passing, 3: Attacking) | Returns: List with points in sections """
        section = max(1, min(3, int(section)))
        teamMults = []
        for i in range(1,12):
            teamMults.append(math.ceil(self.getPlayerOverall(i) * self.getMultipliers(i)[section-1] * self.getPlayer(i).energy))

        return teamMults
    def getPlayerPoints(self, id:int, section:int) -> int:
        """ Returns: Points of the player for their position IN FORMATION (1-11) """
        id = max(1, min(11, int(id)))
        section = max(1, min(3, int(section)))
        return math.ceil(self.getPlayerOverall(id) * self.getMultipliers(id)[section-1] * self.getPlayer(id).energy)
        