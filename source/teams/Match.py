from source.teams.Team import Team
import random
import math

class Match:
    def __init__(self, team1:int=1, team2:int=1):
        """ Starts a Match object | Returns: self """
        self.teams = [Team.get(int(team1)), Team.get(int(team2))]
        # teams[0]: Local team - teams[1]: Away team
        self.score = [0,0]
        self.factor = random.uniform(0.75, 1.35)
        # Random factor for match simulation
    def __str__(self):
        """ Returns: Match object into a readable string: "Real Madrid CF 2 - 3 FC Barcelona" """
        return f"{self.teams[0].name} {self.score[0]} - {self.score[1]} {self.teams[1].name}"
    def poisson(self, lam) -> int:
        """ Takes expected goals and turns them into a random number | Returns: Random goals """
        L = math.exp(-lam)
        k = 0
        p = 1

        while p > L:
            k += 1
            p *= random.random()

        return k - 1
    def getTeamStrenght(self, team:int) -> int:
        """ Calculates team strenght by their section points | Returns: Team strenght int """
        team = max(1, min(2, int(team)))
        oppTeam = 2
        if team == 2: 
            oppTeam = 1

        return (
            self.teams[team-1].formation.getPoints(3) * 0.5 +
            self.teams[team-1].formation.getPoints(2) * 0.35 + 
            self.teams[team-1].formation.getPoints(1) * 0.15 -
            self.teams[oppTeam-1].formation.getPoints(1) * 0.3
        )
    def getExpectedGoals(self, team:int) -> float:
        """ Calculates expected goals for a eam | Returns: Expected goals float """
        return self.getTeamStrenght(team) / (175 * self.factor)
    def simulate(self) -> Team:
        """ Simluates events in a match | Returns: Winner Team object or None if they tie """
        self.score[0] = self.poisson(self.getExpectedGoals(1))
        self.score[1] = self.poisson(self.getExpectedGoals(2))

        if self.score[1] > self.score[0]:
            return self.teams[1]
        elif self.score[0] > self.score[1]:
            return self.teams[0]
        else:
            return None
        