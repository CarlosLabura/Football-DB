
from source.persons.Player import Player
from source.teams.Team import Team
from source.persons.Contract import Contract
# from source.teams.Transfer import Transfer

import csv
def loadTeams(path:str):
    with open(path, mode="r", encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(archivo)

        for fila in lector_csv:
            tm = Team(fila["id"], fila["name"], int(fila["nation"]))
            tm.abbreviation = fila["abbreviation"]
            tm.state = fila["state"]
            tm.setFundation(fila["fundation"])
            tm.budget = int(fila["budget"])
            tm.formationID = int(fila["formation"])
def loadPlayers(path:str):
    with open(path, mode="r", encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(archivo)

        for fila in lector_csv:
            plr = Player(fila["id"], fila["name"], fila["surname"], fila["birth"])
            plr.commonName = fila["commonName"]

            nations = fila["nations"].replace(" ", "").split(",")
            for nation in nations:
                plr.addNation(nation)

            plr.setBody(fila["height"], fila["weight"])
            plr.setStatsFoot(fila["left"], fila["right"])

            plr.potential = int(fila["potential"])

            plr.setStatsPace(fila["acceleration"], fila["speed"], fila["resistance"])
            plr.setStatsShooting(fila["finishing"], fila["curve"], fila["power"])
            plr.setStatsPassing(fila["accuracy"], fila["cross"], fila["vision"])
            plr.setStatsDribbling(fila["dribble"], fila["skill"], fila["control"])
            plr.setStatsDefending(fila["tackle"], fila["slide"], fila["header"])
            plr.setStatsPhysical(fila["jump"], fila["strength"], fila["resistance"])
            plr.setStatsGoalkeeping(fila["dive"], fila["catch"], fila["reflexes"])

            plr.setStatsOther(fila["leadership"], fila["sharpness"], fila["reputation"])

            positions = fila["positions"].replace(" ", "").split(",")
            for position in positions:
                plr.addPosition(position)
def loadContracts(path:str):
    with open(path, mode="r", encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(archivo)

        for fila in lector_csv:
            con = Contract(fila["id"], fila["player"], fila["team"], fila["end"], fila["start"])
            con.wage = int(fila["wage"])
            con.number = int(fila["number"])
            con.setJersey(fila["name"])

# todo:
# competition
# match, simulation
# formations
# managers, id, playstyle
# statistics

# LOAD ORDER
# comps
# teams
# players
# contracts
# formations
# managers

loadTeams("database/teams/Teams.csv")
loadPlayers("database/persons/Players.csv")
loadContracts("database/persons/Contracts.csv")

def printCard(playerID:int):
    plr = Player.get(playerID)

    print(f"{plr.getName()}: {plr.getPlayerOverall()} OVR ({plr.getPositions()[0]["abbreviation"]})")
    print(f" - Pace: {plr.pace}")
    print(f" - Shooting: {plr.shooting}")
    print(f" - Passing: {plr.passing}")
    print(f" - Dribbling: {plr.dribbling}")
    print(f" - Defense: {plr.defending}")
    print(f" - Physical: {plr.physical}")

def printTeam(teamID:int):
    team = Team.get(teamID)

    for player in team.contracts:
        print(team.contracts[player])

def printSet(st:set):
    for element in st:
        print(element)

barca = Team.get(2)
barca.setFormation(barca.formationID)
formation = [
                    [1, 12],
    [5, 16],    [3, 15],   [4, 14],   [2, 13],
                    [6, 17],
            [7, 19],        [8, 18],
    [11, 22],       [10, 21],       [12, 20]
]
for position in formation:
    barca.formation.changePlayer(position[0], position[1])

print(barca.formation.getPositionInFormation("5"))