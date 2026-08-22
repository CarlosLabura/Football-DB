currentYear:int     =  2026
currentMonth:int    =  1
currentDay:int      =  1

class Date:
    def compare(date1:Date, date2:Date) -> bool:
        """
        Compares if date1 is higher than date2
        | Returns: Boolean or None (if they are equals)
        """
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
        """
        Returns the difference between the first date and the second date (which is usally the current one)
        | Returns: The diference (int)
        """
        if type(date) != Date or type(current) != Date:
            print("Date.age(): Wrong date type")
            return

        age = current.year - date.year
        if current.month < date.month or current.month == date.month and current.day <  date.day:
            age -= 1

        return age
    def birthday(date:Date, current:Date) -> bool:
        """
        Checks if the first date is the same as the second date (which is usally the current one)
        | Returns: Boolean with the comparison
        """
        if type(date) != Date or type(current) != Date:
            print("Date.birthday(): Wrong date type")
            return
        
        return current.month == date.month and current.day == date.day
    def parse(string:str="1/1/2000") -> Date:
        """
        Turns a string type of date ("01/01/2000" for example) into an actual Date object
        | Returns: Date object transformed
        """
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
        """
        Starts a Date objects
        | Returns: self
        """
        self.setYear(year)
        self.setMonth(month)
        self.setDay(day)
    def __str__(self):
        """
        Returns: Date object into a readable string: "01/01/2000" (exmaple)
        """
        return f"{self.day}/{self.month}/{self.year}"
    def setYear(self, year:int=2000) -> int:
        """
        Sets the date year, also checking if its a leap year
        | Returns: current year after the method
        """
        year = int(year)
        
        self.leapYear = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        self.year = year
        return self.year
    def setMonth(self, month:int=1) -> int:
        """
        Sets the date month, also checking the days each month has
        | Returns: current month after the method
        """
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
        return self.month
    def setDay(self, day:int=1) -> int:
        """
        Sets the date day
        | Returns: current day after the method
        """
        day = int(day)
        
        self.day = max(1, min(self.monthLimit, day))
        return self.day
    def passMonths(self, times:int=1) -> int:
        """
        Passes months by the times asked, also passings years if needed
        | Returns: current month after the method
        """
        self.month += int(times)

        if self.month > 12:
            self.month = 1
            self.year += 1
            self.setYear(self.year)
            self.setMonth(self.month)
            return self.month

        self.setMonth(self.month)
        return self.month
    def passDays(self, times:int=1) -> int:
        """
        Passes days by the times asked, also passing months if needed
        | Returns: current day after the method
        """
        self.day += int(times)

        if self.day > self.monthLimit:
            self.day = 1
            self.passMonths()
            return self.day
        return self.day
current:Date = Date(currentDay,currentMonth,currentYear)
""" Virtual current date """