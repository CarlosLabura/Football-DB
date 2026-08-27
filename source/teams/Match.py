from source.teams.Team import Team
from source.persons.Player import Player
import random
import math


class Event:
    Goal = 1
    Sub = 2
    Card = 2
    Injury = 4

class Match:
    def __init__(self, team1:int=1, team2:int=1, simulate:bool=False) -> Match:
        """ Starts a Match object | Returns: self """
        self.teams = [Team.get(int(team1)), Team.get(int(team2))]
        self.teams[0].formation.reset()
        self.teams[1].formation.reset()
        """ [0]: Local team - [1]: Away team """ 
        self.score = [0,0]
        self.forcedScore = None
        """ Forced score, goals will automatically simulate from this result"""
        self.penals = [0,0]
        """ Penalties scored in penalty shootouts """
        self.factor = random.uniform(0.75, 1.75)
        """ Random factor for match simulation (0: crazy result, 2: normal result) """ 

        self.events = []
        """ Events of the match ("type", "player", "team", "time", "info") ("info" depends on the event)  """

        self.windows = [int(3), int(3)]
        self.subs = [int(5), int(5)]

        self.minutes = int(90)
        self.minutesExtra = int(120)
        self.extra = bool(False)
        """ Match can go to extra time """
        self.penalties = bool(False)
        """ Go to penalties if teams tie """
        self.penaltiesTaken = []
        """ [0] Player [1] Team [2] Was goal """

        self.showEvents = bool(True)
    
        if bool(simulate):
            self.simulate()
    def __str__(self):
        """ Returns: Match object into a readable string and show events if asked """
        events = ""
        if self.showEvents:
            for event in self.events:
                if event["type"]  == Event.Goal:
                    events = events + f" - GOAL: {Player.get(event["player"]).getName()} ({self.teams[event["team"]].name}) {event["time"]}'\n"
                elif event["type"] == Event.Sub:
                    events = events + f" - SUB: <- {Player.get(event["info"]).getName()} | -> {Player.get(event["player"]).getName()} {event["time"]}'\n"
                
        if self.penalties and self.score[0] == self.score[1]:
                return f"{self.teams[0].name} {self.score[0]} ({self.penals[0]}) - ({self.penals[1]}) {self.score[1]} {self.teams[1].name} \n{events}"

        return f"{self.teams[0].name} {self.score[0]} - {self.score[1]} {self.teams[1].name} \n{events}"
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
    def getRandomPlayer(self, team: int, section: int, excluded: list = None) -> int:
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
    def getBestPlayer(self, team:int, position:int) -> int:
        """ Returns: Best sub player (id) available for a position """
        team = max(1, min(2, int(team)))-1
        bestPlayer:Player
        first = True

        outlist = []
        for out in self.teams[team].formation.changed:
            outlist.append(out[1])
            
        for player in self.teams[team].formation.available:
            if first:
                bestPlayer = Player.get(player)
                first = False
            if Player.get(player).getPositionOverall(self.teams[team].formation.getPosition(position)["name"]) > bestPlayer.getPositionOverall(self.teams[team].formation.getPosition(position)["name"]) and Player.get(player).id not in outlist:
                bestPlayer = Player.get(player)

        return bestPlayer.id
    def simulateEvents(self, start:int, end:int):
        start = int(start)
        end = int(end)

        matchGoals = [0,0]
        if self.forcedScore != None:
            matchGoals[0] = self.forcedScore[0]
            matchGoals[1] = self.forcedScore[1]
        else:
            matchGoals[0] = self.poisson(self.getExpectedGoals(1))
            matchGoals[1] = self.poisson(self.getExpectedGoals(2))

        for team in range(1,3):
            # GOALS
            for _ in range(matchGoals[team-1]):
                self.goal(team, self.getRandomPlayer(team, 3), self.getRandomPlayer(team, 2), random.randint(start, end))

            # SUBS
            windows = random.randint(0, self.windows[team-1])
            self.windows[team-1] -= windows
            for _ in range(self.windows[team-1]):
                minute = random.randint(int(end/2), end)
                for i in range(random.randint(0, self.subs[team-1])):
                    if random.randint(1, 100) == 1:
                        self.sub(team, 1, self.getBestPlayer(team, 1), minute)
                    else:
                        position = random.randint(2, 11)
                        self.sub(team, position, self.getBestPlayer(team, position), minute)
    def simulate(self) -> Team:
        """ Simluates events in a match | Returns: Winner Team object or None if they tie """
        self.simulateEvents(1, self.minutes)

        if self.extra and self.score[0] == self.score[1]:
            self.factor = random.uniform(0.5, 1)
            self.simulateEvents(self.minutes, self.minutesExtra)

        if self.penalties and self.score[0] == self.score[1]:
            return self.penaltyShootout()

        if self.score[1] > self.score[0]:
            return self.teams[1]
        elif self.score[0] > self.score[1]:
            return self.teams[0]
        else:
            return None
    def event(self, type:int, player:int, team:int, time:int, info) -> dict:
        """ Adds an event to the events list | Returns: Event dict """
        team = max(1, min(2, int(team)))-1
        data = {
            "type": int(type),
            "player": int(player),
            "team": team+1,
            "time": int(time),
            "info": info
        }
        self.events.append(data)
        self.events.sort(key=lambda event: event["time"])
        return data
    def fixEvents(self, time:int):
        """ Changes the events of a player from ceratin time """
        for event in self.events:
            if event["time"] > int(time):
                for change in self.teams[event["team"]-1].formation.changed:
                    if event["player"] == change[1]:
                        event["player"] = change[0]
    def goal(self, team:int, player:int, asistant:int, time:int) -> Player:
        """ Scores a goal, setting a player as the scorer | Returns: Scorer Player object """
        team = max(1, min(2, int(team)))-1
        self.score[team] += 1
        self.event(Event.Goal, player, team, time, int(asistant))
        return Player.get(int(player))
    def sub(self, team:int, position:int, player:int, time:int) -> Player:
        """ Sub a player into the formation of a team | Returns: Subbed out Player object """
        team = max(1, min(2, int(team)))-1
        sub = self.teams[team].formation.changePlayer(position, player)
        self.subs[team] -= 1
        self.event(Event.Sub, player, team, time, sub.id)
        self.fixEvents(time)
        return sub
    def penaltyShootout(self) -> Team:
        """ In case of tie, untie with a penalty shootout | Return: Winning Team object"""
        exclude = [[], []]

        def shootPenality(team: int) -> bool:
            """ Returns: Penalty accerted """
            team = max(1, min(2, int(team)))

            if len(exclude[team-1]) >= 11:
                exclude[team-1].clear()

            player = self.getRandomPlayer(team, 3, exclude[team-1])
            penalty = random.random() < 0.50 + Player.get(player).shooting * 0.003
            self.penaltiesTaken.append([player, team, penalty])
            exclude[team-1].append(player)

            if penalty:
                self.penals[team-1] += 1

            return penalty

        for i in range(5):
            shootPenality(1)

            remain2 = 5 - i
            if self.penals[0] > self.penals[1] + remain2:
                return self.teams[0]

            shootPenality(2)

            remain1 = 4 - i
            if self.penals[1] > self.penals[0] + remain1:
                return self.teams[1]

        # Sudden Death
        while self.penals[0] == self.penals[1]:
            shootPenality(1)
            shootPenality(2)

        return self.teams[0] if self.penals[0] > self.penals[1] else self.teams[1]
    def printPenalties(self):
        for penalty in self.penaltiesTaken:
            print(f"{Player.get(penalty[0]).getName()} ({Team.get(penalty[1]).name}): {penalty[2]}")
        
        