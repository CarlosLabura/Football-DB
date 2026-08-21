"""
from source.persons.Player import Player
from source.teams.Team import Team

class Transfer:
    history = []

    def parse(id:int) -> str:
        hist = Transfer.history[int(id)]
        player = Player.get(hist[0])

        return f"{player.name} {player.surname} ({player.id}) | {Team.get(hist[2]).name} -> {Team.get(hist[1]).name} (${hist[3]})"

    def transfer(playerID:int=0, teamID:int=0, jersey:int=99, cost:int=1, wage:int=5000, length:int=1):
        playerID, teamID, jersey, cost, wage, length = int(playerID), int(teamID), int(jersey), int(cost), int(wage), int(length)

        player = Player.get(playerID)
        team = Team.get(teamID)

        if team.budget < cost:
            print(f"Transfer.transfer({player.name} {player.surname} [{player.id}]): {team.name} has not enough budget, returning")
            return

        if team.type == 1:
            oldTeam = Team.get(player.teams["club"]["id"])
            oldTeam.budget += cost
            team.budget -= cost
            
            player.teams["club"] = {"id": teamID, "jersey": jersey, "length": length, "wage": wage}
            Transfer.history.append([playerID, teamID, oldTeam.id, cost])
        elif team.type == 2:
            # if played 3 matches cannot play
            player.teams["national"] = {"id": teamID, "jersey": jersey, "length": 1, "wage": 0}
        elif team.type == 3:
            player.otherTeams.append({"id": teamID, "jersey": jersey, "length": 99, "wage": 0})

        team.addPlayer(playerID)
"""