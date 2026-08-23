from source.teams.Team import Team
# WIP
class Competition:
    ids = {}
    def get(id:int=0) -> Competition:
        return Competition.ids[int(id)]

    def __init__(self, id:int, name:str="", nationID:int = 1) -> Competition:
        self.id = int(id or len(Competition.ids)+1)
        self.name = str(name)
        self.nationID = int(nationID)

        self.multiplier = 0

        self.teamsIDS = set()
        self.knockouts = False
        self.groups = 1

        Competition.ids[self.id] = self

    def addTeam(self, teamID:int=1):
        self.teamsIDS.add(int(teamID))
    
    def getTeams(self) -> list:
        if len(self.teamsIDS) < 1: 
            print(f"Competition.getTeams({self.id}): No teams in {self.name}")
            return None
        
        teamsInfo = []
        for teamID in self.teamsIDS:
            teamsInfo.append(Team.get(teamID))

        return teamsInfo
