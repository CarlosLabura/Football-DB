from source.persons.Person import Person
import source.persons.Position as Position
import math

class Player(Person):
    ids = {}
    """ Dict where all Player objects are stored by its id """
    @staticmethod
    def get(id:int=0) -> Player:
        """ Get a Player object by its id | Returns: Player object """
        return Player.ids[int(id)]
    def __init__(self, id:int, name:str, surname:str, birth:str) -> Player:
        """ Starts a Player object | Returns: self """
        super().__init__(name, surname, birth)
        self.id = int(id or len(Player.ids)+1)

        self.positions = set()
        """ Positions ids """
        self.potential = 0
        """ Potential overall to grow """
        self.contracts = {}
        """ All team Contracts Objects, stored by their ids (self.contracts[2] = Team.get(2) Contract) """

        self.setStatsFoot(1,1)
        self.setStatsPace(1,1,1)
        self.setStatsShooting(1,1,1)
        self.setStatsPassing(1,1,1)
        self.setStatsDribbling(1,1,1)
        self.setStatsDefending(1,1,1)
        self.setStatsPhysical(1,1,1)
        self.setStatsGoalkeeping(1,1,1)
        self.setStatsOther(1,1,1)

        self.energy = 1

        Player.ids[self.id] = self
    def __str__(self):
        """ Returns: Player object into a readable string: "Marc Cucurella (2): 86 OVR ['LB', 'LM'], Spain, 22/7/1998 (27)" """
        return f"{self.getName()} ({self.id}): {self.getOverall()} OVR {[x["abbreviation"] for x in self.getPositions()]}, {self.getNationsInfo()[0]["common_name"]}, {self.birth} ({self.age()})\n - Pace: {self.pace}\n - Shooting: {self.shooting}\n - Passing: {self.passing}\n - Dribbling: {self.dribbling}\n - Defense: {self.defending}\n - Physical: {self.physical}"
    def addPosition(self, name:str) -> dict:
        """ Adds a position this player can play | Returns: Position dict """
        self.positions.add(name)
        return Position.getPosition(name)
    def getPositions(self) -> list:
        """ Returns: List of Position dicts this player can play """
        if len(self.positions) < 1:
            print(f"Player.getPositions({self.getName()} [{self.id}]): Player has no positions assigned, returning None")
            return None

        positionsInfo = []
        for posID in self.positions:
            positionsInfo.append(Position.getPosition(posID))

        return positionsInfo
    def getPositionOverall(self, pos:str) -> int:
        """ Returns: Players overall in a specific position """
        return math.ceil(((self.leftFoot * Position.getPositionRate(pos, "leftFoot") 
                    + self.rightFoot * Position.getPositionRate(pos, "rightFoot") 
                    + self.pace * Position.getPositionRate(pos, "pace") 
                    + self.shooting * Position.getPositionRate(pos, "shooting") 
                    + self.passing * Position.getPositionRate(pos, "passing") 
                    + self.dribbling * Position.getPositionRate(pos, "dribbling") 
                    + self.defending * Position.getPositionRate(pos, "defending") 
                    + self.physical * Position.getPositionRate(pos, "physical") 
                    + self.goalkeeping * Position.getPositionRate(pos, "goalkeeping"))
                    / (Position.getPositionRate(pos, "leftFoot") 
                       + Position.getPositionRate(pos, "rightFoot") 
                       + Position.getPositionRate(pos, "pace") 
                       + Position.getPositionRate(pos, "shooting") 
                       + Position.getPositionRate(pos, "passing") 
                       + Position.getPositionRate(pos, "dribbling") 
                       + Position.getPositionRate(pos, "defending") 
                       + Position.getPositionRate(pos, "physical") 
                       + Position.getPositionRate(pos, "goalkeeping")
                    ) 
                    + self.sharpness) / 2)
    def getOverall(self) -> int:
        """ Returns: Players overall """
        ovrs = []
        for position in self.positions:
            ovrs.append(self.getPositionOverall(position))

        return math.ceil(sum(ovrs) / len(ovrs))
    def getValue(self) -> int:
        """ Returns: Player value in market """
        # wip
        pass
    def setStatsFoot(self, leftFoot:int, rightFoot:int) -> bool:
        """ Sets Foot attributes | Returns: Is player left footed """
        self.leftFoot = int(leftFoot or self.leftFoot)
        self.rightFoot = int(rightFoot or self.rightFoot)
        return (leftFoot > rightFoot)
    def setStatsPace(self, acceleration:int, speed:int, resistance:int):
        """ Sets Pace attributes | Returns: Attribute overall """
        self.acceleration = int(acceleration or self.acceleration)
        self.speed = int(speed or self.speed)
        self.resistance = int(resistance or self.resistance)

        self.pace = math.ceil((self.acceleration + self.speed + self.resistance) / 3)
        return self.pace
    def setStatsShooting(self, finishing:int, curve:int, power:int):
        """ Sets Shooting attributes | Returns: Attribute overall """
        self.finishing = int(finishing or self.finishing)
        self.curve = int(curve or self.curve)
        self.power = int(power or self.power)

        self.shooting = math.ceil((self.finishing + self.curve + self.power) / 3)
        return self.shooting
    def setStatsPassing(self, accuracy:int, cross:int, vision:int):
        """ Sets Passing attributes | Returns: Attribute overall """
        self.accuracy = int(accuracy or self.accuracy)
        self.cross = int(cross or self.cross) 
        self.vision = int(vision or self.vision)

        self.passing = math.ceil((self.accuracy + self.cross + self.vision) / 3)
        return self.passing
    def setStatsDribbling(self, dribble:int, skill:int, control:int):
        """ Sets Dribbling attributes | Returns: Attribute overall """
        self.dribble = int(dribble or self.dribble)
        self.skill = int(skill or self.skill)
        self.control = int(control or self.control)

        self.dribbling = math.ceil((self.dribble + self.skill + self.control) / 3)
        return self.dribbling
    def setStatsDefending(self, tackle:int, slide:int, header:int):
        """ Sets Defensive attributes | Returns: Attribute overall """
        self.tackle = int(tackle or self.tackle)
        self.slide = int(slide or self.slide)
        self.header = int(header or self.header)

        self.defending = math.ceil((self.tackle + self.slide + self.header) / 3)
        return self.defending
    def setStatsPhysical(self, jump:int, strength:int, resistance:int):
        """ Sets Physical attributes | Returns: Attribute overall """
        self.jump = int(jump or self.jump)
        self.strength = int(strength or self.strength)
        self.resistance = int(resistance or self.resistance)

        self.physical = math.ceil((self.jump + self.strength + self.resistance) / 3)
        return self.physical
    def setStatsGoalkeeping(self, dive:int, catch:int, reflexes:int):
        """ Sets Goalkeeping attributes | Returns: Attribute overall """
        self.dive = int(dive or self.dive)
        self.catch = int(catch or self.catch)
        self.reflexes = int(reflexes or self.reflexes)

        self.goalkeeping = math.ceil((self.dive + self.catch + self.reflexes) / 3)
        return self.goalkeeping
    def setStatsOther(self, leadership:int, sharpness:int, reputation:int):
        """ Sets Other attributes """
        self.leadership = int(leadership or self.leadership)
        self.sharpness = int(sharpness or self.sharpness)
        self.reputation = int(reputation or self.reputation)