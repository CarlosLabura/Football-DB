
from source.persons.Player import Player
from source.teams.Team import Team
from source.teams.Formation import Formation
from source.persons.Contract import Contract
from source.teams.Match import Match

import csv
# in databases in case of repearing the ids the last database loaded will take the place
def loadTeams(path:str) -> csv.DictReader:
    """ Loads the Teams database from the path selected | Returns: Database content"""
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            tm = Team(row["id"], row["name"], int(row["nation"]))
            tm.setAbbreviation(row["abbreviation"])
            tm.state = row["state"]
            tm.setFundation(row["fundation"])
            tm.budget = int(row["budget"])
        return database
def loadPlayers(path:str) -> csv.DictReader:
    """ Loads the Players database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            plr = Player(row["id"], row["name"], row["surname"], row["birth"])
            plr.commonName = row["commonName"]

            nations = row["nations"].replace(" ", "").split(",")
            for nation in nations:
                plr.addNation(nation)

            plr.setBody(row["height"], row["weight"])
            plr.setStatsFoot(row["left"], row["right"])

            plr.potential = int(row["potential"])

            plr.setStatsPace(row["acceleration"], row["speed"], row["resistance"])
            plr.setStatsShooting(row["finishing"], row["curve"], row["power"])
            plr.setStatsPassing(row["accuracy"], row["cross"], row["vision"])
            plr.setStatsDribbling(row["dribble"], row["skill"], row["control"])
            plr.setStatsDefending(row["tackle"], row["slide"], row["header"])
            plr.setStatsPhysical(row["jump"], row["strength"], row["resistance"])
            plr.setStatsGoalkeeping(row["dive"], row["catch"], row["reflexes"])

            plr.setStatsOther(row["leadership"], row["sharpness"], row["reputation"])

            positions = row["positions"].replace(" ", "").split(",")
            for position in positions:
                plr.addPosition(position)
        return database
def loadContracts(path:str) -> csv.DictReader:
    """ Loads the Contracts database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            con = Contract(row["id"], row["player"], row["team"], row["end"], row["start"])
            con.wage = int(row["wage"])
            con.number = int(row["number"])
            con.setJersey(row["name"])
        return database
def loadTeamsFormation(path:str) -> csv.DictReader:
    with open(path, mode="r", encoding="utf-8") as file:
        database = csv.DictReader(file)

        for row in database:
            form = Team.get(row["team"]).setFormation(row["formation"])
            for i in range(1,12):
                form.changePlayer(i, row["pos"+str(i)])
        return database

########################################################
# LOAD ORDER
# comps
# teams
# players
# contracts
# formations
# managers (id, playstyles)
# statistics

loadTeams("database/teams/Teams.csv")
loadPlayers("database/persons/Players.csv")
loadContracts("database/persons/Contracts.csv")
loadTeamsFormation("database/teams/TeamsFormation.csv")
########################################################

# DEBUG FUNCTIONS
def printCard(player:int) -> Player:
    """ Prints the player (id) individual stats and his overall rating | Returns: Player object """
    plr = Player.get(player)

    print(plr)
    print(f" - Pace: {plr.pace}")
    print(f" - Shooting: {plr.shooting}")
    print(f" - Passing: {plr.passing}")
    print(f" - Dribbling: {plr.dribbling}")
    print(f" - Defense: {plr.defending}")
    print(f" - Physical: {plr.physical}")
    return plr
def printTeam(team:int) -> Team:
    """ Prints players in a team (id) | Returns: Team object """
    tm = Team.get(team)

    for player in tm.contracts:
        print(tm.contracts[player])
    return tm
def printSet(st:set):
    """ Prints elements in any set """
    for element in st:
        print(element)


""" 
MADRID
379
493
322

BARCA
432
573
309
"""



for i in range(1,100):
    mtch = Match(1,2)
    mtch.simulate()
    print(mtch)
