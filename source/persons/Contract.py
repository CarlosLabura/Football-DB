from source.persons.Player import Player
from source.teams.Team import Team
from source.world.Date import Date
from source.world.Date import current as currentDate

class Contract:
    ids = {}
    def get(id:int=0) -> Contract:
        return Contract.ids[int(id)]

    def __init__(self, id:int, player:int, team:int, end:str, start:str = ""):
        self.id = int(id or len(Contract.ids)+1)

        self.player = Player.get(int(player))
        self.team = Team.get(int(team))
        self.end = Date.parse(str(end))

        self.wage = 0

        self.number = 0
        self.setJersey()

        if start == "":
            self.start = currentDate
        else:
            self.start = Date.parse(str(start))

        self.player.contracts[self.team.id] = self
        self.team.contracts[self.player.id] = self
        Contract.ids[self.id] = self

    def __str__(self):
        return f"{self.player.getName()} ({self.team.name}) | Start: {self.start} | End: {self.end}"

    def newContract(self, team:int, end:str, wage:int = 0, number:int = 0, jersey:str = ""):
        if self.team.id == int(team):
            print(f"Contract.newContract({self.player.getName()} [{self.id}]): Cannot do a new contract for the same team")
            return

        self.end = Date.parse(str(end))
        self.start = currentDate
        self.wage = int(wage)
        self.number = int(number)
        self.setJersey(str(jersey))
        self.changeTeam(int(team))

    def changeTeam(self, team:int):
        self.team.contracts[self.player.id] = None
        self.player.contracts[self.team.id] = None

        self.team = Team.get(int(team))
        self.player.contracts[self.team.id] = self
        self.team.contracts[self.player.id] = self

    def expandContract(self, date:str):
        self.end = Date.parse(str(date))

    def setJersey(self, custom:str = ""):
        if custom != "":
            self.name = custom
        elif self.player.commonName != "":
            self.name = self.player.commonName
        else:
            self.name = self.player.surname

    def getTimeLeft(self) -> int:
        return Date.age(self.start, self.end)
        
