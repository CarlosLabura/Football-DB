from source.persons.Player import Player
from source.teams.Team import Team
from source.world.Date import Date
from source.world.Date import current as currentDate

class Contract:
    ids = {}
    """ Dict where all Contract objects are stored by its id """
    @staticmethod
    def get(id:int=0) -> Contract:
        """ Get a Contract object by its id | Returns: Contract object """
        return Contract.ids[int(id)]
    def __init__(self, id:int, player:int, team:int, end:str, start:str = "") -> Contract:
        """ Starts a Contract object | Returns: self """
        self.id = int(id or len(Contract.ids)+1)
        self.player = Player.get(int(player))
        """ Player object tied to the contract """
        self.team = Team.get(int(team))
        """ Team object tied to the contract """
        self.end = Date.parse(str(end))
        """ Contract end Date object """
        
        self.start:Date
        """ Contract start Date object """
        if start == "":
            self.start = currentDate
        else:
            self.start = Date.parse(str(start))

        self.wage = int(0)

        self.number = int(0)
        """ Jersey number """
        self.name = str("")
        """ Jersey name """
        self.setJersey()

        self.player.contracts[self.team.id] = self
        self.team.contracts[self.player.id] = self
        Contract.ids[self.id] = self
    def __str__(self):
        """ Returns: Contract object into a readable string: "Juan Gonzalez (FC Barcelona) | Start: 1/1/2000 | End: 1/1/2005" """
        return f"{self.player.getName()} ({self.team.name}) | Start: {self.start} | End: {self.end}"
    def transfer(self, team:int, end:str, wage:int = 0, number:int = 0, jersey:str = "", fee:int = 0) -> Team:
        """ Transfer player to another team | Returns: Old Team object """
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
        lastTeam = self.changeTeam(int(team), int(fee))
        return lastTeam
    def changeTeam(self, team:int, fee:int = 0) -> Team:
        """ Changes the Team contract for another with a fee | Returns: Old Team object """
        oldTeam = self.team
        self.team.budget += int(fee)
        self.team.contracts[self.player.id] = None
        self.player.contracts[self.team.id] = None

        self.team = Team.get(int(team))
        self.player.contracts[self.team.id] = self
        self.team.contracts[self.player.id] = self
        self.team.budget -= int(fee)
        return oldTeam
    def expandContract(self, date:str) -> Date:
        """ Changes the Contract end | Returns: New parsed contract end Date """
        self.end = Date.parse(str(date))
        return self.end
    def setJersey(self, custom:str = "") -> str:
        """ Sets the jersey name | Returns: Jersey name string """
        if str(custom) != "":
            self.name = str(custom)
        elif self.player.commonName != "":
            self.name = self.player.commonName
        else:
            self.name = self.player.surname
        return self.name
    def getTimeLeft(self) -> int:
        """ Returns: Number of year left until the end of the contract """
        return Date.age(self.start, self.end)
        
