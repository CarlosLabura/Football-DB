from source.world.Date import Date
import source.world.Nation as Nation
from source.teams.Formation import Formation

defaultTeamName = "Free Agents"
class Team:
    ids = {}
    def get(id:int=0) -> Team:
        return Team.ids[int(id)]

    def __init__(self, id:int, name:str=defaultTeamName, nationID:int=1) -> Team:
        self.id = int(id or len(Team.ids)+1)
        self.name = str(name)
        self.abbreviation = self.name[:3].upper()

        self.nationID = int(nationID)
        self.state = ""
        self.setFundation("1/1/2000")

        self.budget = 0

        self.contracts = {}
        self.formationID = 0
        # self.setFormation(0)

        Team.ids[self.id] = self

    def __str__(self):
        return f"Team({self.id}): {self.name}, {self.getNationInfo()["common_name"]}"

    def setFormation(self, formation:int):
        playerList = set()
        for plr in self.contracts:
            playerList.add(self.contracts[plr].player.id)

        self.formation = Formation(int(formation), playerList)

    def setAbbreviation(self, string:str="XXX"):
        self.abbreviation = str(string)[:3].upper()

    def setFundation(self, date:str= "1/1/2000"):
        self.fundation = Date.parse(str(date))

    def getNationInfo(self) -> dict:
        if self.nationID != None:
            return Nation.getNationInfo(self.nationID)
        print(f"Team.getNationInfo({self.id}): No nations assigned, returning None")
        return None
Team(0, "Free Agents", 186)
