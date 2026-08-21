from source.teams.Team import Team
from source.persons.Player import Player

class Match:
    def __init__(self, team1ID:int=1, team2ID:int=1):
        self.team1ID = int(team1ID)
        self.team1Goals = 0

        self.team2ID = int(team2ID)
        self.team2Goals = 0

        self.goals = []
        
        self.simulate()

    def simulate(self):
        pass

    def getScore(self) -> str:
        return f"{self.team1Goals} - {self.team2Goals}"

    def goal(self, scorerID:int=1, assisterID:int=1):
        scorerID = int(scorerID)
        scorer = Player.get(scorerID)

        types = ["clubs", "national", "other"]

        fromTeam2 = False
        for typ in types:
            if scorer.teams[types[typ]]["id"] == self.team2ID:
                fromTeam2 = True
                break

        if fromTeam2:
            self.team2Goals += 1
        else:
            self.team1Goals += 1
            
        self.goals.append([scorerID, int(assisterID)])