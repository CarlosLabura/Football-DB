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

    def transfer(self, team:int, end:str, wage:int = 0, number:int = 0, jersey:str = "", fee:int = 0):
        if self.team.id == int(team):
            print(f"Contract.transfer({self.player.getName()} [{self.id}]): Cannot transfer to the same team")
            return

        if Team.get(int(team)).budget < int(fee):
            print(f"Contract.transfer({self.player.getName()} [{self.id}]): Team has not enough budget")
            return

        self.end = Date.parse(str(end))
        self.start = currentDate
        self.wage = int(wage)
        self.number = int(number)
        self.setJersey(str(jersey))
        self.changeTeam(int(team), int(fee))

    def changeTeam(self, team:int, fee:int = 0):
        self.team.wage += int(fee)
        self.team.contracts[self.player.id] = None
        self.player.contracts[self.team.id] = None

        self.team = Team.get(int(team))
        self.player.contracts[self.team.id] = self
        self.team.contracts[self.player.id] = self
        self.team.wage -= int(fee)

    def expandContract(self, date:str):
        self.end = Date.parse(str(date))

    def setJersey(self, custom:str = ""):
        if str(custom) != "":
            self.name = str(custom)
        elif self.player.commonName != "":
            self.name = self.player.commonName
        else:
            self.name = self.player.surname

    def getTimeLeft(self) -> int:
        return Date.age(self.start, self.end)
        
