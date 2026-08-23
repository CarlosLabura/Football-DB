from source.world.Date import Date
import source.world.Nation as Nation
from source.teams.Formation import Formation

defaultTeamName = "Free Agents"
class Team:
    ids = {} 
    """ Dict where all Team objects are stored by its id """
    def get(id:int=0) -> Team:
        """ Get a Team object by its id | Returns: Team object """
        return Team.ids[int(id)]
    def __init__(self, id:int, name:str=defaultTeamName, nationID:int=1) -> Team:
        """ Starts a Team object | Returns: self """
        self.id = int(id or len(Team.ids)+1)
        self.name = str(name)
        self.setAbbreviation(self.name)

        self.nationID = int(nationID)
        """ Teams nation id, use GetNationInfo() to get Nation dict """
        self.state = ""
        self.setFundation("1/1/2000")

        self.budget = 0
        """ Transfer budget """
        self.contracts = {}
        """ All player Contracts Objects, stored by their ids (self.contracts[11] = Player.get(11) Contract) """
        Team.ids[self.id] = self
    def __str__(self):
        """ Returns: Team object into a readable string: "Team(1): FC Barcelona (Spain)" (exmaple) """
        return f"Team({self.id}): {self.name}, {self.getNationInfo()["common_name"]}"
    def setFormation(self, formation:int) -> Formation:
        """ Sets the team formation by its id | Returns: Formation object """
        playerList = set()
        for plr in self.contracts:
            playerList.add(self.contracts[plr].player.id)

        self.formation = Formation(int(formation), playerList)
        return self.formation
    def setAbbreviation(self, string:str="XXX") -> str:
        """ Sets the correct format for the abbreviation | Returns: Formatted abbreviation """
        self.abbreviation = str(string)[:3].upper()
        return self.abbreviation
    def setFundation(self, date:str= "1/1/2000") -> Date:
        """ Sets the fundation date by a string | Returns: Date object """
        self.fundation = Date.parse(str(date))
        return self.fundation
    def getNationInfo(self) -> dict:
        """ Returns: Teams Nation dict """
        if self.nationID != None:
            return Nation.getNationInfo(self.nationID)
        print(f"Team.getNationInfo({self.id}): No nation assigned, returning None")
        return None
Team(0, "Free Agents", 186)
