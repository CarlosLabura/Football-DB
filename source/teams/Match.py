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
        """ [0]: Local team - [1]: Away team """ 
        self.teams[0].formation.reset()
        self.teams[1].formation.reset()
        self.activePlayers = [
            self.teams[0].formation.players.copy(),
            self.teams[1].formation.players.copy(),
        ]
        self.substitutionPositions = [{}, {}]
        """ Positions already substituted by team and minute """
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
        """ Show match events in print """
    
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
        team = max(0, min(1, int(team)))
        oppTeam = 1
        if team == 1: 
            oppTeam = 0

        return (
            self.teams[team].formation.getPoints(3) * 0.5 +
            self.teams[team].formation.getPoints(2) * 0.35 + 
            self.teams[team].formation.getPoints(1) * 0.15 -
            self.teams[oppTeam].formation.getPoints(1) * 0.3 -
            self.teams[oppTeam].formation.getPlayerOverall(1) * 0.2
        )
    def getExpectedGoals(self, team:int) -> float:
        """ Calculates expected goals for a eam | Returns: Expected goals """
        return self.getTeamStrenght(team) / (175 * self.factor)
    def getRandomPlayer(self, team: int, section: int, excluded: list = None) -> int:
        """ Chooses a random player depending on the play section (Defending, Passing, Attacking) | Returns: Random Player id """
        team = max(0, min(1, int(team)))
        section = max(1, min(3, int(section)))

        if excluded is None:
            excluded = []

        playerVariation = 1.0

        points = self.teams[team].formation.getTeamPoints(section)

        players = []
        weights = []

        for position in range(1, 12):
            player = self.teams[team].formation.players[position]
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
        team = max(0, min(1, int(team)))
        bestPlayer:Player
        first = True
            
        for player in self.teams[team].formation.available:
            if first:
                bestPlayer = Player.get(player)
                first = False
            if Player.get(player).getPositionOverall(self.teams[team].formation.getPosition(position)["name"]) > bestPlayer.getPositionOverall(self.teams[team].formation.getPosition(position)["name"]):
                bestPlayer = Player.get(player)

        return bestPlayer.id
    def simulateEvents(self, start:int, end:int):
        """ Simulates events from a minute to another """
        start = int(start)
        end = int(end)

        matchGoals = [0,0]
        if self.forcedScore != None:
            matchGoals[0] = self.forcedScore[0]
            matchGoals[1] = self.forcedScore[1]
        else:
            matchGoals[0] = self.poisson(self.getExpectedGoals(1))
            matchGoals[1] = self.poisson(self.getExpectedGoals(2))

        # EVENTS
        for team in range(2):
            # GOALS
            for _ in range(matchGoals[team]):
                self.goal(team, self.getRandomPlayer(team, 3), self.getRandomPlayer(team, 2), random.randint(start, end))

            # SUBS
            windows = random.randint(0, self.windows[team])
            self.windows[team] -= windows
            for _ in range(windows):
                minute = random.randint(int(end/2), end)
                usedPositions = self.substitutionPositions[team].setdefault(minute, set())
                for i in range(random.randint(0, self.subs[team])):
                    availablePositions = [
                        position for position in range(2, 12)
                        if position not in usedPositions
                    ]
                    if not availablePositions:
                        break
                    if random.randint(1, 200) == 1:
                        position = 1
                    else:
                        position = random.choice(availablePositions)
                    if position in usedPositions:
                        break

                    self.sub(team, position, self.getBestPlayer(team, position), minute)
                    usedPositions.add(position)
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
        team = max(0, min(1, int(team)))
        data = {
            "type": int(type),
            "player": int(player),
            "team": team,
            "time": int(time),
            "info": info
        }
        self.events.append(data)
        self.events.sort(key=lambda event: event["time"])
        return data
    def fixEvents(self, time:int) -> int:
        """ Changes the events of a player from ceratin time | Returns: Events changed """
        eventsChanged = 0
        for event in self.events:
            if event["time"] > int(time) and event["type"] != Event.Sub:
                for change in self.teams[event["team"]].formation.changed:
                    if event["player"] == change[1]:
                        event["player"] = change[0]
                        eventsChanged += 1
        return eventsChanged
    def goal(self, team:int, player:int, asistant:int, time:int) -> Player:
        """ Scores a goal, setting a player as the scorer | Returns: Scorer Player object """
        team = max(0, min(1, int(team)))
        self.score[team] += 1
        self.event(Event.Goal, player, team, time, int(asistant))
        return Player.get(int(player))
    def sub(self, team:int, position:int, player:int, time:int) -> Player:
        """ Sub a player into the formation of a team | Returns: Subbed out Player object """
        team = max(0, min(1, int(team)))
        outgoing = self.activePlayers[team][position]
        self.teams[team].formation.changePlayer(position, player)
        self.activePlayers[team][position] = int(player)
        self.subs[team] -= 1
        self.event(Event.Sub, player, team, time, outgoing)
        self.fixEvents(time)
        return Player.get(outgoing)
    def penaltyShootout(self) -> Team:
        """ In case of tie, untie with a penalty shootout | Return: Winning Team object"""
        exclude = [[], []]
        def shootPenality(team: int) -> bool:
            """ Returns: Penalty accerted """
            team = max(0, min(1, int(team)))

            if len(exclude[team]) >= 11:
                exclude[team].clear()

            player = self.getRandomPlayer(team, 3, exclude[team])
            penalty = random.random() < 0.50 + Player.get(player).shooting * 0.003
            self.penaltiesTaken.append([player, team, penalty])
            exclude[team].append(player)

            if penalty:
                self.penals[team] += 1

            return penalty

        for i in range(5):
            shootPenality(0)

            remain2 = 5 - i
            if self.penals[0] > self.penals[1] + remain2:
                return self.teams[0]

            shootPenality(1)

            remain1 = 4 - i
            if self.penals[1] > self.penals[0] + remain1:
                return self.teams[1]

        # Sudden Death
        while self.penals[0] == self.penals[1]:
            shootPenality(0)
            shootPenality(1)

        return self.teams[0] if self.penals[0] > self.penals[1] else self.teams[1]
    def printPenalties(self):
        for penalty in self.penaltiesTaken:
            print(f"{Player.get(penalty[0]).getName()} ({Team.get(penalty[1]).name}): {penalty[2]}")
        
        