from source.world.Date import Date
import source.world.Nation as Nation

defaultTeamName = "Free Agents"
class Team:
    ids = {}
    def get(id:int=0) -> Team:
        return Team.ids[int(id)]

    def __init__(self, id:int, name:str=defaultTeamName, nationID:int=1, type:int = 1) -> Team:
        self.id = int(id or len(Team.ids)+1)
        self.name = str(name)
        self.abbreviation = self.name[:3].upper()

        self.nationID = int(nationID)
        self.state = ""
        self.setFundation("1/1/2000")

        self.budget = 0

        self.contracts = {}

        Team.ids[self.id] = self

    def __str__(self):
        return f"Team({self.id}): {self.name}, {self.getNationInfo()["common_name"]}"
    
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
