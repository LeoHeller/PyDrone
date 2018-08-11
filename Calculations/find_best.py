import json

class optimizer():
    def __init__(self,file_name):
        self.file_name = file_name
        self.file = self.load_file()
        self.best = ""
        self.find_best()

    def load_file(self):
        with open(self.file_name, "r") as fi:
            return json.load(fi)
    
    def find_best(self):
        highscore = 0
        for block in self.file:
            cblock = self.file[block]
            if cblock["efficiency"] and  cblock["power"] and cblock["thrust"] and cblock["weight"] != "0":
                try:
                    score = self.calculate_score(cblock["efficiency"], cblock["power"], cblock["thrust"], cblock["weight"])
                except ZeroDivisionError:
                    print(cblock)
                if score > highscore:
                    self.best = block
                    highscore = score
        print(self.best)

    def calculate_score(self, eff, power, thrust, weight):
        score = float(eff)/float(weight) +float(eff)/float(thrust)
        return score


optimizer("motors.json")
