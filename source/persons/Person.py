from source.world.Date import Date 
from source.world.Date import current as currentDate
import source.world.Nation as Nation

class Person:
    def __init__(self, name:str="Unknown", surname:str="Unknown", birth:str="1/1/2000") -> Person:
        self.name = str(name)
        self.surname = str(surname)
        self.commonName = ""
        self.birth = Date.parse(str(birth))
        self.setBody(180, 80)
        self.nationsID = set()
    
    def __str__(self):
        return f"Person({self.getName()}): {self.birth} ({self.age()})"

    def getName(self) -> str:
        if self.commonName != "":
            return self.commonName

        return f"{self.name} {self.surname}"

    def addNation(self, nationID:int=1):
        nationID = int(nationID)
        
        if nationID > len(Nation.nations) or nationID < 1:
            print(f"Person.addNation({self.getName()}): Nation unknown, Setting automatically to 1 (Afghanistan)")
            nationID = 1
            
        self.nationsID.add(nationID)

    def getNationsInfo(self) -> list:
        if len(self.nationsID) < 1:
            print(f"Person.getNationsInfo({self.getName()}): Person has no nations assigned, returning None")
            return None

        nationsInfo = []
        for nationID in self.nationsID:
            nationsInfo.append(Nation.getNationInfo(nationID))

        return nationsInfo
    
    def age(self) -> int:
        return Date.age(self.birth, currentDate)
    
    def setBody(self, height:int, weight:int):
        self.weight = int(weight or self.weight)
        self.height = int(height or self.height)