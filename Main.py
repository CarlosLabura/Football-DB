
from source.persons.Player import Player
from source.teams.Team import Team
from source.persons.Contract import Contract

import csv
# in databases in case of repearing the ids the last database loaded will take the place
def loadTeams(path:str) -> csv.DictReader:
    """ Loads the Teams database from the path selected | Returns: Database content"""
    with open(path, mode="r", encoding="utf-8") as archivo:
        file = csv.DictReader(archivo)

        for row in file:
            tm = Team(row["id"], row["name"], int(row["nation"]))
            tm.setAbbreviation(row["abbreviation"])
            tm.state = row["state"]
            tm.setFundation(row["fundation"])
            tm.budget = int(row["budget"])
        return file
def loadPlayers(path:str) -> csv.DictReader:
    """ Loads the Players database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as archivo:
        file = csv.DictReader(archivo)

        for row in file:
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
        return file
def loadContracts(path:str) -> csv.DictReader:
    """ Loads the Contracts database from the path selected | Returns: Database content """
    with open(path, mode="r", encoding="utf-8") as archivo:
        file = csv.DictReader(archivo)
        print(file)

        for row in file:
            con = Contract(row["id"], row["player"], row["team"], row["end"], row["start"])
            con.wage = int(row["wage"])
            con.number = int(row["number"])
            con.setJersey(row["name"])
        return file

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
########################################################

# DEBUG FUNCTIONS
def printCard(playerID:int) -> Player:
    """ Prints the player (id) individual stats and his overall rating | Returns: Player object """
    plr = Player.get(playerID)

    print(f"{plr.getName()}: {plr.getPlayerOverall()} OVR ({plr.getPositions()[0]["abbreviation"]})")
    print(f" - Pace: {plr.pace}")
    print(f" - Shooting: {plr.shooting}")
    print(f" - Passing: {plr.passing}")
    print(f" - Dribbling: {plr.dribbling}")
    print(f" - Defense: {plr.defending}")
    print(f" - Physical: {plr.physical}")
    return plr
def printTeam(teamID:int) -> Team:
    """ Prints players in a team (id) | Returns: Team object """
    team = Team.get(teamID)

    for player in team.contracts:
        print(team.contracts[player])
    return team
def printSet(st:set):
    """ Prints elements in any set """
    for element in st:
        print(element)

""" # EXAMPLE
barca = Team.get(2)
barca.setFormation(barca.formationID)
formation = [
                    [1, 12],
    [5, 16],    [3, 15],   [4, 14],   [2, 13],
                    [7, 17],
            [6, 19],        [8, 18],
    [11, 22],       [10, 21],       [9, 20]
]
for position in formation:
    barca.formation.changePlayer(position[0], position[1])

for i in range(1,12):
    print(barca.formation.getPlayer(i).getName() + ": " + str(barca.formation.getPlayerOverall(i)))
"""