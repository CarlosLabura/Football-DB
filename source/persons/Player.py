from source.persons.Person import Person
import source.persons.Position as Position
import math

class Player(Person):
    ids = {}
    def get(id:int=0) -> Player:
        return Player.ids[int(id)]

    def __init__(self, id:int, name:str, surname:str, birth:str) -> Player:
        super().__init__(name, surname, birth)
        self.id = int(id or len(Player.ids)+1)

        self.positions = set()
        self.potential = 0

        self.contracts = {}

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
        return f"Player({self.getName()} [{self.id}]): {self.birth} ({self.age()})"

    def addPosition(self, pos:str):
        self.positions.add(pos)

    def getPositions(self):
        if len(self.positions) < 1:
            print(f"Player.getPositions({self.getName()} [{self.id}]): Player has no positions assigned, returning None")
            return None

        positionsInfo = []
        for posID in self.positions:
            positionsInfo.append(Position.getPosition(posID))

        return positionsInfo

    def getOverall(self, pos:str) -> int:
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

    def getPlayerOverall(self):
        ovrs = []
        for position in self.positions:
            ovrs.append(self.getOverall(position))

        return math.ceil(sum(ovrs) / len(ovrs))

    def getValue(self):
        pass

    def setStatsFoot(self, leftFoot:int, rightFoot:int):
        self.leftFoot = int(leftFoot or self.leftFoot)
        self.rightFoot = int(rightFoot or self.rightFoot)

    def setStatsPace(self, acceleration:int, speed:int, resistance:int):
        self.acceleration = int(acceleration or self.acceleration)
        self.speed = int(speed or self.speed)
        self.resistance = int(resistance or self.resistance)

        self.pace = math.ceil((self.acceleration + self.speed + self.resistance) / 3)

    def setStatsShooting(self, finishing:int, curve:int, power:int):
        self.finishing = int(finishing or self.finishing)
        self.curve = int(curve or self.curve)
        self.power = int(power or self.power)

        self.shooting = math.ceil((self.finishing + self.curve + self.power) / 3)
    
    def setStatsPassing(self, accuracy:int, cross:int, vision:int):
        self.accuracy = int(accuracy or self.accuracy)
        self.cross = int(cross or self.cross) 
        self.vision = int(vision or self.vision)

        self.passing = math.ceil((self.accuracy + self.cross + self.vision) / 3)
    
    def setStatsDribbling(self, dribble:int, skill:int, control:int):
        self.dribble = int(dribble or self.dribble)
        self.skill = int(skill or self.skill)
        self.control = int(control or self.control)

        self.dribbling = math.ceil((self.dribble + self.skill + self.control) / 3)
    
    def setStatsDefending(self, tackle:int, slide:int, header:int):
        self.tackle = int(tackle or self.tackle)
        self.slide = int(slide or self.slide)
        self.header = int(header or self.header)

        self.defending = math.ceil((self.tackle + self.slide + self.header) / 3)

    def setStatsPhysical(self, jump:int, strength:int, resistance:int):
        self.jump = int(jump or self.jump)
        self.strength = int(strength or self.strength)
        self.resistance = int(resistance or self.resistance)

        self.physical = math.ceil((self.jump + self.strength + self.resistance) / 3)

    def setStatsGoalkeeping(self, dive:int, catch:int, reflexes:int):
        self.dive = int(dive or self.dive)
        self.catch = int(catch or self.catch)
        self.reflexes = int(reflexes or self.reflexes)

        self.goalkeeping = math.ceil((self.dive + self.catch + self.reflexes) / 3)

    def setStatsOther(self, leadership:int, sharpness:int, reputation:int):
        self.leadership = int(leadership or self.leadership)
        self.sharpness = int(sharpness or self.sharpness)
        self.reputation = int(reputation or self.reputation)
Player(0, "Juan", "Gonzalez", "1/1/2000")