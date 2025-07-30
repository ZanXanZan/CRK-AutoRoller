class Stat:
    def __init__(self, stat, percentage):
        self.stat = stat
        self.percentage = percentage
    
    def getNum(self):
        return float(self.percentage.replace("%", ""))
    
    def isValid(self):
        val = self.getNum()
        if self.stat == "ATK":
            return 3 <= val <= 7.5
        elif self.stat == "DEF":
            return 5 <= val <= 7.5
        elif self.stat == "HP":
            return 3 <= val <= 15
        elif self.stat == "ATK SPD":
            return 3 <= val <= 10
        elif self.stat == "CRIT%":
            return 3 <= val <= 7
        elif self.stat == "DMG Resist":
            return 5 <= val <= 10
        elif self.stat == "CRIT Resist":
            return 4 <= val <= 10
        elif self.stat == "Cooldown":
            return 2 <= val <= 6
        elif self.stat == "Amplify Buff" or self.stat == "Debuff Resist":
            return 2 <= val <= 5
        elif self.stat == "DMG Resist Bypass":
            return 5 <= val <= 15
        else:
            return 8 <= val <= 15      
            
            

    def __repr__(self):
        return f"{self.stat} {self.getNum()}"
    