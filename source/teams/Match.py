from source.teams.Team import Team
from source.persons.Player import Player
import random
import math

class Match:
    def __init__(self, team1:int=1, team2:int=1):
        """ Starts a Match object | Returns: self """
        self.teams = [Team.get(int(team1)), Team.get(int(team2))]
        """ [0]: Local team - 1]: Away team """ 
        self.score = [0,0]
        self.forcedScore = None
        """ Forced score """
        self.penals = [0,0]
        """ Penalties scored in penalty shootouts """
        self.factor = random.uniform(0.75, 1)
        """ Random factor for match simulation """ 
        self.goals = []
        """  [0] Goal scorer [1] assistant [2] their team (1-2) [3] time """ 
        self.cards = []
        """  [0] Player [1] Yellow (1) / Red (2) cards [2] Team (1-2) [3] time """ 
        self.injuries = []
        """  [0] Player [1] Injury [2] Team (1-2) [3] time """ 

        self.minutes = int(90)
        self.minutesExtra = int(120)
        self.extra = bool(False)
        """ Match can go to extra time """
        self.penalties = bool(False)
        """ Go to penalties if teams tie """
        self.penaltiesTaken = []
        """ [0] Player [1] Team [2] Was goal """
    def __str__(self):
        """ Returns: Match object into a readable string """
        scorers = ""
        for scorer in self.goals:
            scorers = scorers + f" - GOAL: {Player.get(scorer[0]).getName()} ({self.teams[scorer[2]].name}) {scorer[3]}'\n"

        if self.penalties and self.score[0] == self.score[1]:
            return f"{self.teams[0].name} {self.score[0]} ({self.penals[0]}) - ({self.penals[1]}) {self.score[1]} {self.teams[1].name} \n{scorers}"

        return f"{self.teams[0].name} {self.score[0]} - {self.score[1]} {self.teams[1].name} \n{scorers}"
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
            self.teams[oppTeam-1].formation.getPoints(1) * 0.3 -
            self.teams[oppTeam-1].formation.getPlayerOverall(1) * 0.2
        )
    def getExpectedGoals(self, team:int) -> float:
        """ Calculates expected goals for a eam | Returns: Expected goals float """
        return self.getTeamStrenght(team) / (175 * self.factor)
    def getRandomPlayerBySection(self, team: int, section: int, excluded: list = None) -> int:
        """ Chooses a random player depending on the play section (Defending, Passing, Attacking) | Returns: Random Player id """
        team = max(1, min(2, int(team)))
        section = max(1, min(3, int(section)))

        if excluded is None:
            excluded = []

        playerVariation = 1.0

        points = self.teams[team - 1].formation.getTeamPoints(section)

        players = []
        weights = []

        for position in range(1, 12):
            player = self.teams[team - 1].formation.players[position]
            if player in excluded:
                continue

            weight = max(0, points[position - 1]) ** max(
                0.0,
                float(playerVariation)
            )
            players.append(player)
            weights.append(weight)

        if sum(weights) == 0:
            weights = [1] * len(players)

        return random.choices(
            players,
            weights=weights,
            k=1
        )[0]
    def simulate(self) -> Team:
        """ Simluates events in a match | Returns: Winner Team object or None if they tie """

        matchGoals = [0,0]
        if self.forcedScore != None:
            matchGoals[0] = self.forcedScore[0]
            matchGoals[1] = self.forcedScore[1]
        else:
            matchGoals[0] = self.poisson(self.getExpectedGoals(1))
            matchGoals[1] = self.poisson(self.getExpectedGoals(2))

        for team in range(1,3):
            for i in range(matchGoals[team-1]):
                self.goal(team, self.getRandomPlayerBySection(team, 3), self.getRandomPlayerBySection(team, 2), random.randint(1, self.minutes))

        if self.extra and self.score[0] == self.score[1]:
            self.factor = random.uniform(0.5, 1)

            if self.forcedScore == None:
                matchGoals[0] = self.poisson(self.getExpectedGoals(1))
                matchGoals[1] = self.poisson(self.getExpectedGoals(2))

            for team in range(1,3):
                for i in range(int(matchGoals[team-1]/3)):
                    self.goal(team, self.getRandomPlayerBySection(team, 3), self.getRandomPlayerBySection(team, 2), random.randint(self.minutes, self.minutesExtra))

        if self.penalties and self.score[0] == self.score[1]:
            return self.penaltyShootout()

        if self.score[1] > self.score[0]:
            return self.teams[1]
        elif self.score[0] > self.score[1]:
            return self.teams[0]
        else:
            return None
    def goal(self, team:int, player:int, asistant:int, time:int) -> Player:
        """ Scores a goal, setting a player as the scorer | Returns: Scorer Player object """
        team = max(1, min(2, int(team)))-1
        self.score[team] += 1
        self.goals.append([int(player), int(asistant), team, int(time)])
        self.goals.sort(key=lambda goal: goal[3])
        return Player.get(int(player))
    def printPenalties(self):
        for penalty in self.penaltiesTaken:
            print(f"{Player.get(penalty[0]).getName()} ({Team.get(penalty[1]).name}): {penalty[2]}")
    def penaltyShootout(self) -> Team:
        """ In case of tie, untie with a penalty shootout | Return: Winning Team object"""
        exclude = [[], []]

        def shootPenality(team: int) -> bool:
            """ Returns: Penalty accerted """
            team = max(1, min(2, int(team)))

            if len(exclude[team-1]) >= 11:
                exclude[team-1].clear()

            player = self.getRandomPlayerBySection(team, 3, exclude[team-1])
            penalty = random.random() < 0.50 + Player.get(player).shooting * 0.003
            self.penaltiesTaken.append([player, team, penalty])
            exclude[team-1].append(player)

            if penalty:
                self.penals[team-1] += 1

            return penalty

        for i in range(5):
            shootPenality(1)

            remain2 = 5 - i # Penalties remaining for team 2
            if self.penals[0] > self.penals[1] + remain2:
                return self.teams[0]

            shootPenality(2)

            remain1 = 4 - i # Penalties remaining for team 1
            if self.penals[1] > self.penals[0] + remain1:
                return self.teams[1]

        # Sudden Death
        while self.penals[0] == self.penals[1]:
            shootPenality(1)
            shootPenality(2)

        return self.teams[0] if self.penals[0] > self.penals[1] else self.teams[1]
        
        