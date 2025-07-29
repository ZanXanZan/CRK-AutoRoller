class Stat:
    def __init__(self, stat, percentage):
        self.stat = stat
        self.percentage = percentage
    
    def getNum(self):
        return self.percentage.replace("%", "")

    def __repr__(self):
        return f"{self.stat} {self.getNum()}"