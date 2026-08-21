currentYear:int     =  2026
currentMonth:int    =  1
currentDay:int      =  1

class Date:
    def compare(date1:Date, date2:Date) -> bool:
        if type(date1) != Date or type(date2) != Date:
            print("Date.compare(): Wrong date type")
            return

        if date1.year > date2.year:
            return True
        elif date1.year < date2.year:
            return False
        else:
            if date1.month > date2.month:
                return True
            elif date1.month < date2.month:
                return False
            else:
                if date1.day > date2.day:
                    return True
                elif date1.day < date2.day:
                    return False
                else:
                    return None
    
    def age(date:Date, current:Date) -> int:
        if type(date) != Date or type(current) != Date:
            print("Date.age(): Wrong date type")
            return

        age = current.year - date.year
        if current.month < date.month or current.month == date.month and current.day <  date.day:
            age -= 1

        return age
    
    def birthday(date:Date, current:Date) -> bool:
        if type(date) != Date or type(current) != Date:
            print("Date.birthday(): Wrong date type")
            return
        
        return current.month == date.month and current.day == date.day
    
    def parse(string:str="1/1/2000") -> Date:
        string = str(string)

        if string.count("/") != 2:
            print("Date.parse(): Date must follow DD/MM/YYYY structure, Setting automatically to 1/1/2000")
            string = "1/1/2000"

        string = string.replace(" ", "")
        date = string.split("/")

        for dih in date:
            if dih.isdigit() == False:
                print("Date.parse(): Date must only be numbers, Setting automatically to 1/1/2000")
                date = [1, 1, 2000]
                break

        return Date(int(date[0]), int(date[1]), int(date[2]))
    
    def __init__(self, day:int=1, month:int=1, year:int=2000) -> Date:
        self.setYear(year)
        self.setMonth(month)
        self.setDay(day)

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year}"

    def setYear(self, year:int=2000):
        year = int(year)
        
        self.leapYear = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        self.year = year
    

    def setMonth(self, month:int=1):
        month = int(month)

        months = [
            ["January",     31],
            ["February",    28],
            ["March",       31],
            ["April",       30],
            ["May",         31],
            ["June",        30],
            ["July",        31],
            ["August",      31],
            ["September",   30],
            ["October",     31],
            ["November",    30],
            ["December",    31]
        ]
        if self.leapYear:
            months[1][1] += 1

        self.month = max(1, min(12, month))
        self.monthName = months[self.month-1][0]
        self.monthLimit = months[self.month-1][1]

    def setDay(self, day:int=1):
        day = int(day)
        
        self.day = max(1, min(self.monthLimit, day))

    def passMonths(self, num:int=1):
        self.month += int(num)

        if self.month > 12:
            self.month = 1
            self.year += 1
            self.setYear(self.year)
            self.setMonth(self.month)
            return

        self.setMonth(self.month)

    def passDays(self, num:int=1):
        self.day += int(num)

        if self.day > self.monthLimit:
            self.day = 1
            self.passMonths()
            return

current:Date = Date(currentDay,currentMonth,currentYear)