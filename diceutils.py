# -*- coding: utf-8 -*-

import random

class Die:
    def __init__(self, dieAsList):
        self.m_die = dieAsList
        self.index = 0

    def max(self, symbol):
        values = [face[symbol] for face in self.m_die]
        return max(values)

    def min(self, symbol):
        values = [face[symbol] for face in self.m_die]
        return min(values)

    def proba(self, symbol, equalTo):
        values = [face[symbol] for face in self.m_die]
        count = len([x for x in values if equalTo == x])
        total = len(values)
        return count / total

    def roll(self):
        alea = random.randint(0,len(self.m_die)-1)
        return self.m_die[alea]

    def __iter__(self):
        return iter(self.m_die)

class Dice:
    def __init__(self, diceList):
        self.m_dice = diceList

    def max(self, symbol, modif = 0):
        return sum([ x.max(symbol) for x in self.m_dice ]) + modif

    def min(self, symbol, modif = 0):
        return sum([ x.min(symbol) for x in self.m_dice ]) + modif

    def p(self, result, symbol, modif = 0):
        trueresult = result - modif
        distrib = self.getDistrib(symbol)
        if trueresult in distrib:
            return distrib[trueresult]
        else:
            return 0
            
    def getDistrib(self, symbol):
        histogram = self.getHistogram(symbol)
        distrib = {}
        totalcount = sum( [x for x in histogram.values()] )
        for result, count in histogram.items():
            distrib[result] = count/totalcount
        return distrib

    def getHistogram(self, symbol):
        combinations = Dice._getCombinations(self.m_dice, symbol)
        histogram = {}
        
        for i in range(0, self.max(symbol) + 1):
            histogram[i] = 0
            
        for combi in combinations:
            result = sum( [face[symbol] for face in combi] )
            histogram[result] += 1
        return histogram

    def _getCombinations(dice, symbol, facesSoFar = []):
        if [] == dice:
            return [facesSoFar]
        else:
            combinations = []
            for face in dice[0]:
                combinations += Dice._getCombinations( dice[1:len(dice)], symbol, facesSoFar + [face])
            return combinations

def fight(dice1, dice2, symbol):
    proba1wins = 0
    probadraw = 0
    for a in range(1, dice1.max(symbol) + 1):
        for b in range(0, a):
            print("P("+str(a)+","+str(b)+") = " + str(dice1.p(a, symbol)) + " x " + str(dice2.p(b, symbol)))
            proba1wins += dice1.p(a, symbol)*dice2.p(b, symbol)
    for a in range(0, dice1.max(symbol) +1 ):
        print("P("+str(a)+","+str(a)+") = " + str(dice1.p(a, symbol)) + " x " + str(dice2.p(a, symbol)))
        probadraw += dice1.p(a, symbol)*dice2.p(a, symbol)
            
    return (proba1wins, probadraw)

            
def main():
    print('hello')
    A = Die([{'dmg':0, 'spe':0},
             {'dmg':0, 'spe':0},
             {'dmg':1, 'spe':0},
             {'dmg':1, 'spe':0},
             {'dmg':1, 'spe':0},
             {'dmg':1, 'spe':1}])

    d6 = Die([{'f':1},
              {'f':2},
              {'f':3},
              {'f':4},
              {'f':5},
              {'f':6}])
                                      
    AA = Dice([A,A])
    AAA = Dice([A,A,A])
    D = Dice([d6])
    DD = Dice([d6,d6])
    print(AA.max('dmg', 1))
    print(AA.min('dmg', 3))
    print(AAA.getDistrib('dmg'))
    print(AAA.p(3,'dmg',4))

    print(fight(DD,D,'f') )
    
if __name__ == '__main__':
    exit(main())
