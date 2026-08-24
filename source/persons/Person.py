from source.world.Date import Date 
from source.world.Date import current as currentDate
import source.world.Nation as Nation

class Person:
    def __init__(self, name:str="Unknown", surname:str="Unknown", birth:str="1/1/2000") -> Person:
        """ Starts a Person object | Returns: self """
        self.name = str(name)
        self.surname = str(surname)
        self.commonName = ""
        """ Name used over the full name """
        self.birth = Date.parse(str(birth))
        self.setBody(180, 80)
        self.nationsID = set()
        """ Persons nations id in a set, use GetNationsInfo() to get Nations dict """
    def __str__(self):
        """ Returns: Person object into a readable string: "Juan Gonzalez, 1/1/2000 (26)" """
        return f"{self.getName()}, {self.getNationsInfo()[0]["common_name"]},{self.birth} ({self.age()})"
    def getName(self) -> str:
        """ Returns: Full name or Common name string """
        if self.commonName != "":
            return self.commonName

        return f"{self.name} {self.surname}"
    def addNation(self, nation:int=1) -> dict:
        """ Adds a nation (id) to the Person | Returns: Nation dict """
        nation = int(nation)
        
        if nation > len(Nation.nations) or nation < 1:
            print(f"Person.addNation({self.getName()}): Nation unknown, Setting automatically to 1 (Afghanistan)")
            nation = 1
            
        self.nationsID.add(nation)
        return Nation.getNationInfo(nation)
    def getNationsInfo(self) -> list:
        """ Returns: List of nation dicts of the person """
        if len(self.nationsID) < 1:
            print(f"Person.getNationsInfo({self.getName()}): Person has no nations assigned, returning None")
            return None

        nationsInfo = []
        for nation in self.nationsID:
            nationsInfo.append(Nation.getNationInfo(nation))

        return nationsInfo
    def age(self) -> int:
        """ Returns: Age of the person, calculed from their birthday and the current date """
        return Date.age(self.birth, currentDate)
    def setBody(self, height:int, weight:int) -> float:
        """ Sets the body height and weight | Returns: BMI (???? """
        self.weight = int(weight or self.weight)
        self.height = int(height or self.height)
        return self.weight / (self.height*self.height)