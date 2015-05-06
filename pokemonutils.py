# -*- coding: utf-8 -*-

import csv
import argparse
import copy

from diceutils import *

# low damage, some spe
A = Die([{'dmg':0, 'spe':0},
         {'dmg':0, 'spe':1},
         {'dmg':1, 'spe':0},
         {'dmg':1, 'spe':0},
         {'dmg':1, 'spe':0},
         {'dmg':1, 'spe':0}])

# medium damage
B = Die([{'dmg':0, 'spe':0},
         {'dmg':0, 'spe':0},
         {'dmg':1, 'spe':0},
         {'dmg':1, 'spe':0},
         {'dmg':2, 'spe':0},
         {'dmg':2, 'spe':0}])

# strong die
C = Die([{'dmg':0, 'spe':0},
         {'dmg':1, 'spe':1},
         {'dmg':1, 'spe':0},
         {'dmg':2, 'spe':0},
         {'dmg':2, 'spe':0},
         {'dmg':2, 'spe':0}])

# brutal, no precision
D = Die([{'dmg':0, 'spe':0},
         {'dmg':0, 'spe':0},
         {'dmg':0, 'spe':0},
         {'dmg':1, 'spe':0},
         {'dmg':3, 'spe':0},
         {'dmg':3, 'spe':0}])

# bonus die
E = Die([{'dmg':0, 'spe':0},
         {'dmg':0, 'spe':0},
         {'dmg':0, 'spe':1},
         {'dmg':0, 'spe':1},
         {'dmg':1, 'spe':0},
         {'dmg':1, 'spe':0}])

diceMatrix = {'A':A, 'B':B, 'C':C, 'D':D, 'E':E}
VERBOSE = False

def buildDice(asString):
    dicelist = []
    for character in asString:
        dicelist.append(Die(diceMatrix[character]))
    return Dice(dicelist)

def probaSpe(dice):
    distrib = dice.getDistrib('spe')
    return sum( [y for x, y in distrib.items() if x != 0] )

def makeFight(p1, p2, estimated = -1):
    global VERBOSE
    bonusforp1 = 0
    bonusforp2 = 0
    if (p2["type"] in p1["strength"]) :
        bonusforp1 = 1
    if (p1["type"] in p2["strength"]) :
        bonusforp2 = 1
    (p1w, draw, p2w) = fight(p1["dice"], bonusforp1, p2["dice"], bonusforp2, 'dmg')
    ip1w = int(p1w*100)
    ip2w = int(p2w*100)
    idraw = int(draw*100)
    
    if (estimated == -1):
        print(p1["name"]  + " vs " + p2["name"] + " : " + str(ip1w) + " (" + str(idraw) + ")")
    else:
        if (abs(estimated - ip1w) > 7) or VERBOSE:
            print(p1["name"]  + " vs " + p2["name"] + " : " + str(ip1w) + " (" + str(idraw) + ") ! was estimated : " + str(estimated))
    return (p1w, draw, p2w)
    
def wound(p):
    result = copy.deepcopy(p)
    result['name'] = result['name'] + ' (wounded)'
    dice = result['dice']
    newdice =  Dice( dice.m_dice[0:len(dice.m_dice)-1] )
    result['dice'] = newdice
    return result

def printMostLikely(p):
    distrib = p['dice'].getDistrib('dmg')
    probas = [proba for (value, proba) in distrib.items()]
    probas.sort()

    result = []
    stored = []
    while ((sum(stored) < 0.5)):
        maxproba = max(probas)
        for value, proba in distrib.items():
            if (proba == maxproba):
                result.append((value,int(100* proba)))
                stored.append(proba)
        for i in range(0, probas.count(maxproba)):
            probas.pop()
    return result


def main():
    global VERBOSE
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-c", dest = "csvpath")
    argParser.add_argument("-v", dest = "verbose", action = 'store_true')

    args = argParser.parse_args()

    VERBOSE = args.verbose


    pk = {}
    refpk = {}
    with open(args.csvpath, 'r') as csvfile:

        globalDict = csv.DictReader(csvfile)

        for row in globalDict:
            if (row['name'] != ''):
                diceforthis = buildDice( row['dice'] )
                name = row['name']
                pk[name] = {}
                pk[name]['name'] = name
                pk[name]['dice'] = diceforthis
                pk[name]['strength'] = []
                pk[name]['strength'].append( row['strength1']  )
                pk[name]['strength'].append( row['strength2']  )
                pk[name]['type'] = row['type']
                refpk[row['number']] = name

    # for row in pk.values():
    #     print(row['name'] + ' - spe: ' +  str(int(100*probaSpe(row['dice']))) +
    #           ' - ' + str(row['dice'].min('dmg')) + '-' +  str(row['dice'].max('dmg')) +
    #           ' - ' + str(printMostLikely(row)) )

    # numbers = [int(x) for x in refpk.keys()]
    # numbers.sort()
    # for number in numbers:
    #     name = refpk[str(number)]
    #     pok = pk[name]
    #     print(pok['name'] + ' - spe: ' +  str(int(100*probaSpe(pok['dice']))) +
    #           ' - ' + str(pok['dice'].min('dmg')) + '-' +  str(pok['dice'].max('dmg')) +
    #           ' - ' + str(printMostLikely(pok)) )

    makeFight(pk["Bulbizarre"], pk["Salamèche"], 20)
    makeFight(pk["Bulbizarre"], pk["Magnéti"], 50)
    makeFight(pk["Bulbizarre"], pk["Chenipan"], 30)
    makeFight(pk["Bulbizarre"], pk["Stari"], 60)

    makeFight(pk["Salamèche"], pk["Ponyta"], 50)
    makeFight(pk["Salamèche"], pk["Rhinocorne"], 20)
    makeFight(pk["Salamèche"], pk["Kangourex"], 35)
    makeFight(pk["Salamèche"], pk["Otaria"], 20)

    makeFight(pk["Carapuce"], pk["Otaria"], 50)
    makeFight(pk["Carapuce"], pk["Aspicot"], 60)
    makeFight(pk["Carapuce"], pk["Magmar"], 65)
    makeFight(pk["Carapuce"], pk["Smogo"], 50)
    
    makeFight(pk["Chenipan"], pk["Tadmorv"], 15)
    makeFight(pk["Chenipan"], pk["Elektek"], 40)
    makeFight(pk["Chenipan"], pk["Stari"], 50)

    makeFight(pk["Aspicot"], pk["Kangourex"], 25)
    makeFight(pk["Aspicot"], pk["Leviator"], 15)
    makeFight(pk["Aspicot"], pk["Porygon"], 40)
    
    makeFight(pk["Roucool"], pk["Dracolosse"], 40)
    makeFight(pk["Roucool"], pk["Ptera"], 40)
    makeFight(pk["Roucool"], pk["Bulbizarre"], 70)

    makeFight(pk["Rattata"], pk["Nidoran"], 50)
    makeFight(pk["Rattata"], pk["Otaria"], 50)
    makeFight(pk["Rattata"], pk["Electhor"], 35)

    makeFight(pk["Piafabec"], pk["Nidoking"], 50)
    makeFight(pk["Piafabec"], pk["Paras"], 60)
    makeFight(pk["Piafabec"], pk["Ptera"], 65)
    
    makeFight(pk["Abo"], pk["Voltorbe"], 50)
    makeFight(pk["Abo"], pk["Nidoran"], 50)
    makeFight(pk["Abo"], pk["Tauros"], 35)
    
    makeFight(pk["Pikachu"], pk["Mélofée"], 45)
    makeFight(pk["Pikachu"], pk["Krabby"], 75)
    makeFight(pk["Pikachu"], pk["Mystherbe"], 50)
    


 #   makeFight(pk["Aspicot"], pk["Chenipan"])
 #   makeFight(pk["Roucool"], pk["Chenipan"])
 #   printMostLikely(pk["Aspicot"])


    
if __name__ == '__main__':
    exit(main())
