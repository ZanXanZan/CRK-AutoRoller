from collections import Counter
class Roll:
    def __init__(self, list, valid):
        self.list = list
        self.valid = valid
    
    def sumStats(self):
        sums = {}
        for stat_obj in self.list:
            stat_name = stat_obj.stat
            value = stat_obj.getNum()
            if stat_name in sums:
                sums[stat_name] += value
            else:
                sums[stat_name] = value
        return sums
    
    
    def num_target(self, target):
        counter = 0
        for stat in self.list:
            if stat.stat == target:
                counter += 1
        return counter
    
    def three_check(self):
        stat_names = [stat.stat for stat in self.list]
        counter = Counter(stat_names)
        return any(count >= 3 for count in counter.values())