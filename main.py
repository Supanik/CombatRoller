import random
import os
import io
import json
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader, TabbedPanelItem
try:
    from android.permissions import request_permissions, Permission
except:
    pass
import threading
import time

"""
Request Permissions
"""

try:
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE])

except Exception as e:
    print (e)

"""
Roller Section
"""

class Roller():

    def __init__(self, sides = 20, dice = 1, hitmod = 0, dammod = 0, crit = False, adv = 0):

        self.sides = sides
        self.dice = dice
        self.hitmod = hitmod
        self.dammod = dammod
        self.crit = crit
        self.adv = adv

    def attack(self, sides = 20, mod = 0, adv = 0, improvedcrit = 0):

        """
        hitroll(die sides, hit modification, advantage (-1,0, or 1)
        """
        
        hit = []
        critical = False
        advrolls = 2
        
        for x in range (2):
            hit.append(random.randint(1,sides))

        if adv == 1:
            hitval = max(hit)
            
        if hit[1]<=hit[0] and adv != 1 and adv != -1 or adv == 0 :
            hitval = hit[0]

        if adv == -1:
            hitval = min(hit)

        if hitval == sides:
            critical = True

        if improvedcrit > 2 and improvedcrit < 15 and hitval >= (sides - 1):
            critical = True

        if improvedcrit > 14 and hitval >= (sides - 2):
            critical = True

        if hitval == 1:
            hitmiss = "miss"
        else:
            hitmiss = "hit"
            
        hitval = hitval + mod

        hit = {"To Hit":hitval, "HitMiss":hitmiss, "Critical":critical}
            
        return hit

    def damage(self, crit = False, adv = 0, bruteforce = 0, brutalcrit = 0, devastatingcrit = 0):

        """
        attackroll(number of sides, number of dice, additional damage, critical hit boolean)
        """ 
        sides = self.sides
        advlist = []
        dice = self.dice
        dammod = self.dammod
        damage = {}
        bruteforcecrit = 1
        if crit == True:
            bruteforcecrit = bruteforcecrit * 2
        
        if sides == None or sides == 0 or dice == None or dice == 0:
            return {"Damage":dammod}
        
        advdice = self.dice*2   
        damagelst = []
        

        if crit == True and brutalcrit < 9:
            dice = dice * 2
            advdice = dice * 2

        if crit == True and (brutalcrit > 8 and brutalcrit < 12):
            dice = (dice * 2) + 1
            advdice = dice * 2

        if crit == True and (brutalcrit > 12 and brutalcrit < 17):
            dice = (dice * 2) + 2
            advdice = dice * 2

        if crit == True and brutalcrit > 16:
            dice = (dice * 2) + 3
            advdice = dice * 2
            
            
        if adv == 1 or adv == -1:
            for x in range (advdice):
                advlist.append(random.randint(1,sides))
                
                if len(advlist) > 1 and adv == -1:
                    advlist.sort(reverse = False)
                    damagelst.append(advlist[0])
                    advlist = []

                if len(advlist) > 1 and adv == 1:
                    advlist.sort(reverse = True)
                    damagelst.append(advlist[0])
                    advlist = []

        if adv == 0:
            for x in range (dice):
                damagelst.append(random.randint(1,sides))

        for x in range(bruteforcecrit):

            if bruteforce > 2 and bruteforce < 10 and adv == 0:
                damagelst.append(random.randint(1,4))

            if bruteforce > 2 and bruteforce < 10 and (adv == 1 or adv == -1):
                for x in range (2):
                    advlist.append(random.randint(1,4))

                    if len(advlist) > 1 and adv == -1:
                        advlist.sort(reverse = False)
                        damagelst.append(advlist[0])
                        advlist = []

                    if len(advlist) > 1 and adv == 1:
                        advlist.sort(reverse = True)
                        damagelst.append(advlist[0])
                        advlist = []

            if bruteforce > 9 and bruteforce < 16 and adv == 0:
                damagelst.append(random.randint(1,6))

            if bruteforce > 9 and bruteforce < 16 and (adv == 1 or adv == -1):
                for x in range (2):
                    advlist.append(random.randint(1,6))

                    if len(advlist) > 1 and adv == -1:
                        advlist.sort(reverse = False)
                        damagelst.append(advlist[0])
                        advlist = []

                    if len(advlist) > 1 and adv == 1:
                        advlist.sort(reverse = True)
                        damagelst.append(advlist[0])
                        advlist = []

            if bruteforce > 15 and bruteforce < 20 and adv == 0:
                damagelst.append(random.randint(1,8))

            if bruteforce > 15 and bruteforce < 20 and (adv == 1 or adv == -1):
                for x in range (2):
                    advlist.append(random.randint(1,8))

                    if len(advlist) > 1 and adv == -1:
                        advlist.sort(reverse = False)
                        damagelst.append(advlist[0])
                        advlist = []

                    if len(advlist) > 1 and adv == 1:
                        advlist.sort(reverse = True)
                        damagelst.append(advlist[0])
                        advlist = []

            if bruteforce > 19 and adv == 0:
                damagelst.append(random.randint(1,10))

            if bruteforce > 19 and (adv == 1 or adv == -1):
                for x in range (2):
                    advlist.append(random.randint(1,10))

                    if len(advlist) > 1 and adv == -1:
                        advlist.sort(reverse = False)
                        damagelst.append(advlist[0])
                        advlist = []

                    if len(advlist) > 1 and adv == 1:
                        advlist.sort(reverse = True)
                        damagelst.append(advlist[0])
                        advlist = []

        if crit == True and devastatingcrit > 14:
            damagelst.append(devastatingcrit)
            
        
        if len(damagelst) > 1:
            damage = sum(damagelst)
        elif len(damagelst) == 1:
            damage = damagelst[0]
        
        damage = {"Damage":(damage + dammod)}
        damagelst = []
        advlist = []
        return damage       

def char_roll():
    '''
    Rolls for new character stats
    '''

    char = []

    for x in range(7):
        roll = []
        for x in range(4):
            roll.append(damageroll(6))

        roll.sort()
        del roll[0]

        char.append(sum(roll))

    char.sort()
    del char[0]
    
    return char

"""
Variable Section
"""

crit = False
attackval = {"To Hit": 0, "HitMiss": "hit", "Critical": False}
damage = []
turn = 1
enemyac = 0
simplehistory = []
checkhistory = []
savehistory = []
modifier = 0
multiplier = 1
dice = 1
advantage = {"advantage": 0, "hitadvantage":0, "damadvantage":0}

savepath = "Characters/"
quicksavepath = ""

try:
    os.listdir(path="/sdcard/CombatRoller/")

except:
    try:
        os.mkdir(path="/sdcard/CombatRoller/")

    except:
        pass

try:
    os.listdir(path="/storage/emulated/0/CombatRoller/")
    

except:    
    try:
        os.mkdir(path="/storage/emulated/0/CombatRoller/")
    except:
        pass
    
try:
    filelist = (os.listdir(path="/sdcard/CombatRoller/Characters/"))
    savepath = "/sdcard/CombatRoller/Characters/"
    quicksavepath = "/sdcard/CombatRoller/"

except:    
    try:
        filelist = (os.listdir(path="/storage/emulated/0/CombatRoller/Characters/"))
        savepath = "/storage/emulated/0/CombatRoller/Characters/"
        quicksavepath = "/storage/emulated/0/CombatRoller/"
    except:
        try:
            os.mkdir(path="/storage/emulated/0/CombatRoller/Characters")
            filelist = (os.listdir(path="/storage/emulated/0/CombatRoller/Characters/"))
            savepath = "/storage/emulated/0/CombatRoller/Characters/"
            quicksavepath = "/storage/emulated/0/CombatRoller/"
        except:
            try:
                filelist = (os.listdir(path="Characters/"))
            except:
                pass

try:
    
    with open(quicksavepath + 'QuickSave.txt') as charfile:
            characterfile = json.load(charfile)

except:

    with open('QuickSave.txt') as charfile:
            characterfile = json.load(charfile)

charstatlist = ["Name", "Health", "CurrentHP", "AC", "InitMod",
             "StrMod", "DexMod", "ConMod", "IntMod", "WisMod",
             "ChaMod", "StrSave", "DexSave", "ConSave", "IntSave",
             "WisSave", "ChaSave", "Acrobatics", "AnimalHandling",
             "Arcana", "Athletics", "Deception", "History", "Insight",
             "Intimidation", "Investigation", "Medicine", "Nature",
             "Perception", "Performance", "Persuasion", "Religion",
             "SleightofHand", "Stealth", "Survival", "ToHit", "HitMod",
                "AttackDice", "SpelltoHit", "SpellHitMod", "SpellAttackDice"]

class Character():
        
    def __init__(self, characterfile = characterfile):

        self.name = characterfile["Name"]
        self.health = characterfile["Health"]
        self.currenthp = characterfile["CurrentHP"]
        self.ac = characterfile["AC"]
        self.initmod = characterfile["InitMod"]
        self.strmod = characterfile["StrMod"]
        self.dexmod = characterfile["DexMod"]
        self.conmod = characterfile["ConMod"]
        self.intmod = characterfile["IntMod"]
        self.wismod = characterfile["WisMod"]
        self.chamod = characterfile["ChaMod"]
        self.strsave = characterfile["StrSave"]
        self.dexsave = characterfile["DexSave"]
        self.consave = characterfile["ConSave"]
        self.intsave = characterfile["IntSave"]
        self.wissave = characterfile["WisSave"]
        self.chasave = characterfile["ChaSave"]
        self.acrobatics = characterfile["Acrobatics"]
        self.animalhandling = characterfile["AnimalHandling"]
        self.arcana = characterfile["Arcana"]
        self.athletics = characterfile["Athletics"]
        self.deception = characterfile["Deception"]
        self.history = characterfile["History"]
        self.insight = characterfile["Insight"]
        self.intimidation = characterfile["Intimidation"]
        self.investigation = characterfile["Investigation"]
        self.medicine = characterfile["Medicine"]
        self.nature = characterfile["Nature"]
        self.perception = characterfile["Perception"]
        self.performance = characterfile["Performance"]
        self.persuasion = characterfile["Persuasion"]
        self.religion = characterfile["Religion"]
        self.sleightofhand = characterfile["SleightofHand"]
        self.stealth = characterfile["Stealth"]
        self.survival = characterfile["Survival"]
        
        self.tohit = characterfile["ToHit"]
        self.hitmod = characterfile["HitMod"]
        self.attackdice = characterfile["AttackDice"]

        self.spelltohit = characterfile["SpelltoHit"]
        self.spellhitmod = characterfile["SpellHitMod"]
        self.spellattackdice = characterfile["SpellAttackDice"]

        self.rollinitiative = Roller(20, 1, self.initmod)
        self.rollattack = Roller(self.tohit, self.attackdice, self.hitmod)
        self.rollspellattack = Roller(self.spelltohit, self.spellattackdice, self.spellhitmod)

Player = Character()

actionattrib = ["name", "tohit", "hitmod", "dice", "sides", "damagemod", "improvedcrit", "bruteforce", "brutalcrit", "devastatingcrit", "baseduration", "ammunition"]

def defineactions(characterfile = characterfile):

    actions = []

    actions.append(Roller(characterfile["actions"][0]["sides"], characterfile["actions"][0]["dice"], characterfile["actions"][0]["tohit"], characterfile["actions"][0]["damagemod"]))
    actions[0].name = "Action 1"
    try:
        actions[0].name = characterfile["actions"][0]["name"]
    except:
        pass   
    actions[0].tohit = 20
    try:
        actions[0].tohit = characterfile["actions"][0]["tohit"]
    except:
        pass
    actions[0].hitmod = 0
    try:
        actions[0].hitmod = characterfile["actions"][0]["hitmod"]
    except:
        pass
    actions[0].dice = 1
    try:
        actions[0].dice = characterfile["actions"][0]["dice"]
    except:
        pass
    actions[0].diesides = 6
    try:
        actions[0].diesides = characterfile["actions"][0]["sides"]
    except:
        pass
    actions[0].damagemod = 0
    try:
        actions[0].damagemod = characterfile["actions"][0]["damagemod"]
    except:
        pass
    actions[0].improvedcrit = 0
    try:
        actions[0].improvedcrit = characterfile["actions"][0]["improvedcrit"]
    except:
        pass
    actions[0].bruteforce = 0
    try:
        actions[0].bruteforce = characterfile["actions"][0]["bruteforce"]
    except:
        pass
    actions[0].brutalcrit = 0
    try:
        actions[0].brutalcrit = characterfile["actions"][0]["brutalcrit"]
    except:
        pass
    actions[0].devastatingcrit = 0
    try:
        actions[0].devastatingcrit = characterfile["actions"][0]["devastatingcrit"]
    except:
        pass
    actions[0].baseduration = 0
    try:
        actions[0].baseduration = characterfile["actions"][0]["baseduration"]
    except:
        pass
    actions[0].ammunition = 0
    try:
        actions[0].ammunition = characterfile["actions"][0]["ammunition"]
    except:
        pass
    actions[0].duration = 0

    actions.append(Roller(characterfile["actions"][1]["sides"], characterfile["actions"][1]["dice"], characterfile["actions"][1]["tohit"], characterfile["actions"][1]["damagemod"]))
    actions[1].name = "Action 2"
    try:
        actions[1].name = characterfile["actions"][1]["name"]
    except:
        pass   
    actions[1].tohit = 20
    try:
        actions[1].tohit = characterfile["actions"][1]["tohit"]
    except:
        pass
    actions[1].hitmod = 0
    try:
        actions[1].hitmod = characterfile["actions"][1]["hitmod"]
    except:
        pass
    actions[1].dice = 1
    try:
        actions[1].dice = characterfile["actions"][1]["dice"]
    except:
        pass
    actions[1].diesides = 6
    try:
        actions[1].diesides = characterfile["actions"][1]["sides"]
    except:
        pass
    actions[1].damagemod = 0
    try:
        actions[1].damagemod = characterfile["actions"][1]["damagemod"]
    except:
        pass
    actions[1].improvedcrit = 0
    try:
        actions[1].improvedcrit = characterfile["actions"][1]["improvedcrit"]
    except:
        pass
    actions[1].bruteforce = 0
    try:
        actions[1].bruteforce = characterfile["actions"][1]["bruteforce"]
    except:
        pass
    actions[1].brutalcrit = 0
    try:
        actions[1].brutalcrit = characterfile["actions"][1]["brutalcrit"]
    except:
        pass
    actions[1].devastatingcrit = 0
    try:
        actions[1].devastatingcrit = characterfile["actions"][1]["devastatingcrit"]
    except:
        pass
    actions[1].baseduration = 0
    try:
        actions[1].baseduration = characterfile["actions"][1]["baseduration"]
    except:
        pass
    actions[1].ammunition = 0
    try:
        actions[1].ammunition = characterfile["actions"][1]["ammunition"]
    except:
        pass
    actions[1].duration = 0

    actions.append(Roller(characterfile["actions"][2]["sides"], characterfile["actions"][2]["dice"], characterfile["actions"][2]["tohit"], characterfile["actions"][2]["damagemod"]))
    actions[2].name = "Action 3"
    try:
        actions[2].name = characterfile["actions"][2]["name"]
    except:
        pass   
    actions[2].tohit = 20
    try:
        actions[2].tohit = characterfile["actions"][2]["tohit"]
    except:
        pass
    actions[2].hitmod = 0
    try:
        actions[2].hitmod = characterfile["actions"][2]["hitmod"]
    except:
        pass
    actions[2].dice = 1
    try:
        actions[2].dice = characterfile["actions"][2]["dice"]
    except:
        pass
    actions[2].diesides = 6
    try:
        actions[2].diesides = characterfile["actions"][2]["sides"]
    except:
        pass
    actions[2].damagemod = 0
    try:
        actions[2].damagemod = characterfile["actions"][2]["damagemod"]
    except:
        pass
    actions[2].improvedcrit = 0
    try:
        actions[2].improvedcrit = characterfile["actions"][2]["improvedcrit"]
    except:
        pass
    actions[2].bruteforce = 0
    try:
        actions[2].bruteforce = characterfile["actions"][2]["bruteforce"]
    except:
        pass
    actions[2].brutalcrit = 0
    try:
        actions[2].brutalcrit = characterfile["actions"][2]["brutalcrit"]
    except:
        pass
    actions[2].devastatingcrit = 0
    try:
        actions[2].devastatingcrit = characterfile["actions"][2]["devastatingcrit"]
    except:
        pass
    actions[2].baseduration = 0
    try:
        actions[2].baseduration = characterfile["actions"][2]["baseduration"]
    except:
        pass
    actions[2].ammunition = 0
    try:
        actions[2].ammunition = characterfile["actions"][2]["ammunition"]
    except:
        pass
    actions[2].duration = 0

    actions.append(Roller(characterfile["actions"][3]["sides"], characterfile["actions"][3]["dice"], characterfile["actions"][3]["tohit"], characterfile["actions"][3]["damagemod"]))
    actions[3].name = "Action 4"
    try:
        actions[3].name = characterfile["actions"][3]["name"]
    except:
        pass   
    actions[3].tohit = 20
    try:
        actions[3].tohit = characterfile["actions"][3]["tohit"]
    except:
        pass
    actions[3].hitmod = 0
    try:
        actions[3].hitmod = characterfile["actions"][3]["hitmod"]
    except:
        pass
    actions[3].dice = 1
    try:
        actions[3].dice = characterfile["actions"][3]["dice"]
    except:
        pass
    actions[3].diesides = 6
    try:
        actions[3].diesides = characterfile["actions"][3]["sides"]
    except:
        pass
    actions[3].damagemod = 0
    try:
        actions[3].damagemod = characterfile["actions"][3]["damagemod"]
    except:
        pass
    actions[3].improvedcrit = 0
    try:
        actions[3].improvedcrit = characterfile["actions"][3]["improvedcrit"]
    except:
        pass
    actions[3].bruteforce = 0
    try:
        actions[3].bruteforce = characterfile["actions"][3]["bruteforce"]
    except:
        pass
    actions[3].brutalcrit = 0
    try:
        actions[3].brutalcrit = characterfile["actions"][3]["brutalcrit"]
    except:
        pass
    actions[3].devastatingcrit = 0
    try:
        actions[3].devastatingcrit = characterfile["actions"][3]["devastatingcrit"]
    except:
        pass
    actions[3].baseduration = 0
    try:
        actions[3].baseduration = characterfile["actions"][3]["baseduration"]
    except:
        pass
    actions[3].ammunition = 0
    try:
        actions[3].ammunition = characterfile["actions"][3]["ammunition"]
    except:
        pass
    actions[3].duration = 0

    actions.append(Roller(characterfile["actions"][4]["sides"], characterfile["actions"][4]["dice"], characterfile["actions"][4]["tohit"], characterfile["actions"][4]["damagemod"]))
    actions[4].name = "Action 5"
    try:
        actions[4].name = characterfile["actions"][4]["name"]
    except:
        pass   
    actions[4].tohit = 20
    try:
        actions[4].tohit = characterfile["actions"][4]["tohit"]
    except:
        pass
    actions[4].hitmod = 0
    try:
        actions[4].hitmod = characterfile["actions"][4]["hitmod"]
    except:
        pass
    actions[4].dice = 1
    try:
        actions[4].dice = characterfile["actions"][4]["dice"]
    except:
        pass
    actions[4].diesides = 6
    try:
        actions[4].diesides = characterfile["actions"][4]["sides"]
    except:
        pass
    actions[4].damagemod = 0
    try:
        actions[4].damagemod = characterfile["actions"][4]["damagemod"]
    except:
        pass
    actions[4].improvedcrit = 0
    try:
        actions[4].improvedcrit = characterfile["actions"][4]["improvedcrit"]
    except:
        pass
    actions[4].bruteforce = 0
    try:
        actions[4].bruteforce = characterfile["actions"][4]["bruteforce"]
    except:
        pass
    actions[4].brutalcrit = 0
    try:
        actions[4].brutalcrit = characterfile["actions"][4]["brutalcrit"]
    except:
        pass
    actions[4].devastatingcrit = 0
    try:
        actions[4].devastatingcrit = characterfile["actions"][4]["devastatingcrit"]
    except:
        pass
    actions[4].baseduration = 0
    try:
        actions[4].baseduration = characterfile["actions"][4]["baseduration"]
    except:
        pass
    actions[4].ammunition = 0
    try:
        actions[4].ammunition = characterfile["actions"][4]["ammunition"]
    except:
        pass
    actions[4].duration = 0

    actions.append(Roller(characterfile["actions"][5]["sides"], characterfile["actions"][5]["dice"], characterfile["actions"][5]["tohit"], characterfile["actions"][5]["damagemod"]))
    actions[5].name = "Action 6"
    try:
        actions[5].name = characterfile["actions"][5]["name"]
    except:
        pass   
    actions[5].tohit = 20
    try:
        actions[5].tohit = characterfile["actions"][5]["tohit"]
    except:
        pass
    actions[5].hitmod = 0
    try:
        actions[5].hitmod = characterfile["actions"][5]["hitmod"]
    except:
        pass
    actions[5].dice = 1
    try:
        actions[5].dice = characterfile["actions"][5]["dice"]
    except:
        pass
    actions[5].diesides = 6
    try:
        actions[5].diesides = characterfile["actions"][5]["sides"]
    except:
        pass
    actions[5].damagemod = 0
    try:
        actions[5].damagemod = characterfile["actions"][5]["damagemod"]
    except:
        pass
    actions[5].improvedcrit = 0
    try:
        actions[5].improvedcrit = characterfile["actions"][5]["improvedcrit"]
    except:
        pass
    actions[5].bruteforce = 0
    try:
        actions[5].bruteforce = characterfile["actions"][5]["bruteforce"]
    except:
        pass
    actions[5].brutalcrit = 0
    try:
        actions[5].brutalcrit = characterfile["actions"][5]["brutalcrit"]
    except:
        pass
    actions[5].devastatingcrit = 0
    try:
        actions[5].devastatingcrit = characterfile["actions"][5]["devastatingcrit"]
    except:
        pass
    actions[5].baseduration = 0
    try:
        actions[5].baseduration = characterfile["actions"][5]["baseduration"]
    except:
        pass
    actions[5].ammunition = 0
    try:
        actions[5].ammunition = characterfile["actions"][5]["ammunition"]
    except:
        pass
    actions[5].duration = 0

    actions.append(Roller(characterfile["actions"][6]["sides"], characterfile["actions"][6]["dice"], characterfile["actions"][6]["tohit"], characterfile["actions"][6]["damagemod"]))
    actions[6].name = "Action 7"
    try:
        actions[6].name = characterfile["actions"][6]["name"]
    except:
        pass   
    actions[6].tohit = 20
    try:
        actions[6].tohit = characterfile["actions"][6]["tohit"]
    except:
        pass
    actions[6].hitmod = 0
    try:
        actions[6].hitmod = characterfile["actions"][6]["hitmod"]
    except:
        pass
    actions[6].dice = 1
    try:
        actions[6].dice = characterfile["actions"][6]["dice"]
    except:
        pass
    actions[6].diesides = 6
    try:
        actions[6].diesides = characterfile["actions"][6]["sides"]
    except:
        pass
    actions[6].damagemod = 0
    try:
        actions[6].damagemod = characterfile["actions"][6]["damagemod"]
    except:
        pass
    actions[6].improvedcrit = 0
    try:
        actions[6].improvedcrit = characterfile["actions"][6]["improvedcrit"]
    except:
        pass
    actions[6].bruteforce = 0
    try:
        actions[6].bruteforce = characterfile["actions"][6]["bruteforce"]
    except:
        pass
    actions[6].brutalcrit = 0
    try:
        actions[6].brutalcrit = characterfile["actions"][6]["brutalcrit"]
    except:
        pass
    actions[6].devastatingcrit = 0
    try:
        actions[6].devastatingcrit = characterfile["actions"][6]["devastatingcrit"]
    except:
        pass
    actions[6].baseduration = 0
    try:
        actions[6].baseduration = characterfile["actions"][6]["baseduration"]
    except:
        pass
    actions[6].ammunition = 0
    try:
        actions[6].ammunition = characterfile["actions"][6]["ammunition"]
    except:
        pass
    actions[6].duration = 0

    actions.append(Roller(characterfile["actions"][7]["sides"], characterfile["actions"][7]["dice"], characterfile["actions"][7]["tohit"], characterfile["actions"][7]["damagemod"]))
    actions[7].name = "Action 8"
    try:
        actions[7].name = characterfile["actions"][7]["name"]
    except:
        pass   
    actions[7].tohit = 20
    try:
        actions[7].tohit = characterfile["actions"][7]["tohit"]
    except:
        pass
    actions[7].hitmod = 0
    try:
        actions[7].hitmod = characterfile["actions"][7]["hitmod"]
    except:
        pass
    actions[7].dice = 1
    try:
        actions[7].dice = characterfile["actions"][7]["dice"]
    except:
        pass
    actions[7].diesides = 6
    try:
        actions[7].diesides = characterfile["actions"][7]["sides"]
    except:
        pass
    actions[7].damagemod = 0
    try:
        actions[7].damagemod = characterfile["actions"][7]["damagemod"]
    except:
        pass
    actions[7].improvedcrit = 0
    try:
        actions[7].improvedcrit = characterfile["actions"][7]["improvedcrit"]
    except:
        pass
    actions[7].bruteforce = 0
    try:
        actions[7].bruteforce = characterfile["actions"][7]["bruteforce"]
    except:
        pass
    actions[7].brutalcrit = 0
    try:
        actions[7].brutalcrit = characterfile["actions"][7]["brutalcrit"]
    except:
        pass
    actions[7].devastatingcrit = 0
    try:
        actions[7].devastatingcrit = characterfile["actions"][7]["devastatingcrit"]
    except:
        pass
    actions[7].baseduration = 0
    try:
        actions[7].baseduration = characterfile["actions"][7]["baseduration"]
    except:
        pass
    actions[7].ammunition = 0
    try:
        actions[7].ammunition = characterfile["actions"][7]["ammunition"]
    except:
        pass
    actions[7].duration = 0

    actions.append(Roller(characterfile["actions"][8]["sides"], characterfile["actions"][8]["dice"], characterfile["actions"][8]["tohit"], characterfile["actions"][8]["damagemod"]))
    actions[8].name = "Action 9"
    try:
        actions[8].name = characterfile["actions"][8]["name"]
    except:
        pass   
    actions[8].tohit = 20
    try:
        actions[8].tohit = characterfile["actions"][8]["tohit"]
    except:
        pass
    actions[8].hitmod = 0
    try:
        actions[8].hitmod = characterfile["actions"][8]["hitmod"]
    except:
        pass
    actions[8].dice = 1
    try:
        actions[8].dice = characterfile["actions"][8]["dice"]
    except:
        pass
    actions[8].diesides = 6
    try:
        actions[8].diesides = characterfile["actions"][8]["sides"]
    except:
        pass
    actions[8].damagemod = 0
    try:
        actions[8].damagemod = characterfile["actions"][8]["damagemod"]
    except:
        pass
    actions[8].improvedcrit = 0
    try:
        actions[8].improvedcrit = characterfile["actions"][8]["improvedcrit"]
    except:
        pass
    actions[8].bruteforce = 0
    try:
        actions[8].bruteforce = characterfile["actions"][8]["bruteforce"]
    except:
        pass
    actions[8].brutalcrit = 0
    try:
        actions[8].brutalcrit = characterfile["actions"][8]["brutalcrit"]
    except:
        pass
    actions[8].devastatingcrit = 0
    try:
        actions[8].devastatingcrit = characterfile["actions"][8]["devastatingcrit"]
    except:
        pass
    actions[8].baseduration = 0
    try:
        actions[8].baseduration = characterfile["actions"][8]["baseduration"]
    except:
        pass
    actions[8].ammunition = 0
    try:
        actions[8].ammunition = characterfile["actions"][8]["ammunition"]
    except:
        pass
    actions[8].duration = 0

    actions.append(Roller(characterfile["actions"][9]["sides"], characterfile["actions"][9]["dice"], characterfile["actions"][9]["tohit"], characterfile["actions"][9]["damagemod"]))
    actions[9].name = "Action 10"
    try:
        actions[9].name = characterfile["actions"][9]["name"]
    except:
        pass   
    actions[9].tohit = 20
    try:
        actions[9].tohit = characterfile["actions"][9]["tohit"]
    except:
        pass
    actions[9].hitmod = 0
    try:
        actions[9].hitmod = characterfile["actions"][9]["hitmod"]
    except:
        pass
    actions[9].dice = 1
    try:
        actions[9].dice = characterfile["actions"][9]["dice"]
    except:
        pass
    actions[9].diesides = 6
    try:
        actions[9].diesides = characterfile["actions"][9]["sides"]
    except:
        pass
    actions[9].damagemod = 0
    try:
        actions[9].damagemod = characterfile["actions"][9]["damagemod"]
    except:
        pass
    actions[9].improvedcrit = 0
    try:
        actions[9].improvedcrit = characterfile["actions"][9]["improvedcrit"]
    except:
        pass
    actions[9].bruteforce = 0
    try:
        actions[9].bruteforce = characterfile["actions"][9]["bruteforce"]
    except:
        pass
    actions[9].brutalcrit = 0
    try:
        actions[9].brutalcrit = characterfile["actions"][9]["brutalcrit"]
    except:
        pass
    actions[9].devastatingcrit = 0
    try:
        actions[9].devastatingcrit = characterfile["actions"][9]["devastatingcrit"]
    except:
        pass
    actions[9].baseduration = 0
    try:
        actions[9].baseduration = characterfile["actions"][9]["baseduration"]
    except:
        pass
    actions[9].ammunition = 0
    try:
        actions[9].ammunition = characterfile["actions"][9]["ammunition"]
    except:
        pass
    actions[9].duration = 0

    return actions

actions = defineactions()

def save(name, savefile):
    global actionattrib
    tmpdict = {}
    tmplist = []
    
    for x in actions:
        tmpdict2 = {}
        for i in actionattrib:
            if i in x.__dict__.keys():
                tmpdict2[i] = (x.__dict__[i])
        tmplist.append(tmpdict2)
                
    for x in charstatlist:
        if x.lower() in Player.__dict__.keys():
            tmpdict[x] = Player.__dict__[x.lower()]

    tmpdict["actions"] = tmplist

    tmpdict["Name"] = name
    
    try:
        with io.open(savefile, 'w', encoding='utf-8') as f:
            f.write(json.dumps(tmpdict, ensure_ascii=False))
    except Exception as e:
        print (e)

"""
Player Section
"""

tohitmod = 0

def PlayerTab():
    layout = GridLayout(cols=2)
    lblchar = Label(text= Player.name +"   " + "HP-" + str(Player.currenthp))
    lblenemy = Label(text= "Enemy    " + "AC-" + str(enemyac))
    lbl = Label(text= "0")
    lbldamage = Label(text= "History")

    if enemyac == 0:
        lblenemy.text = "Enemy    " + "AC-" + "0"
    
    def save_char(self):
        savefile = quicksavepath + 'QuickSave.txt'
        save(Player.name, savefile)

    def increasehitmod(self):
        global tohitmod
        tohitmod += 1
        if tohitmod != 0:
            if tohitmod > 0:
                btnattack.text = "Weapon Attack! " + "+" + str(tohitmod)
                btnspellattack.text = "Spell Attack! " + "+" + str(tohitmod)
            else:
                btnattack.text = "Weapon Attack! " + str(tohitmod)
                btnspellattack.text = "Spell Attack! " + str(tohitmod)
                
        if tohitmod == 0:
            btnattack.text = "Weapon Attack!"
            btnspellattack.text = "Spell Attack!"

    def decreasehitmod(self):
        global tohitmod
        tohitmod -= 1
        if tohitmod != 0:
            if tohitmod > 0:
                btnattack.text = "Weapon Attack! " + "+" + str(tohitmod)
                btnspellattack.text = "Spell Attack! " + "+" + str(tohitmod)
            else:
                btnattack.text = "Weapon Attack! " + str(tohitmod)
                btnspellattack.text = "Spell Attack! " + str(tohitmod)
                
        if tohitmod == 0:
            btnattack.text = "Weapon Attack!"
            btnspellattack.text = "Spell Attack!"
        
        
    def charhealthup(self):
        if Player.currenthp == Player.health or Player.currenthp > Player.health:
            Player.currenthp += 1
            lblchar.text = str(Player.name) +"   " + "HP-" + str(Player.currenthp) + " (" + str(Player.currenthp - Player.health) + " Temp)"
        else:
            Player.currenthp += 1
            lblchar.text = str(Player.name) +"   " + "HP-" + str(Player.currenthp)

    def charhealthdn(self):
        if Player.currenthp > (Player.health + 1):
            Player.currenthp -= 1
            lblchar.text = str(Player.name) +"   " + "HP-" + str(Player.currenthp) + " (" + str(Player.currenthp - Player.health) + " Temp)" 
        else:
            Player.currenthp -= 1
            lblchar.text = str(Player.name) +"   " + "HP-" + str(Player.currenthp)

    def heal(self):
        try:
            if sum(damage) + Player.currenthp > Player.health:
                Player.currenthp = Player.health
            else:
                Player.currenthp = Player.currenthp + sum(damage)
            lblchar.text = Player.name +"   " + "HP-" + str(Player.currenthp)
        except Exception as e:
            print(e)

    def enemyacup(self):
        global enemyac
        enemyac += 1

    def enemyacdn(self):
        global enemyac
        if enemyac > 0:
            enemyac -= 1

    def advantagecheck():
        global advantage
        
        if btnadvantage.state == "down" and btnhitadvantage.state == "down":
            advantage["hitadvantage"] = 1
        elif btndisadvantage.state == "down" and btnhitadvantage.state == "down":
            advantage["hitadvantage"] = -1
        elif btnadvantage.state == "down" and btndamadvantage.state == "down":
            advantage["damadvantage"] = 1
        elif btndisadvantage.state == "down" and btndamadvantage.state == "down":
            advantage["damadvantage"] = -1
        elif btnadvantage.state == "down" and btnhitadvantage.state == "normal" and btndamadvantage.state == "normal":
            advantage["hitadvantage"] = 1
            advantage["damadvantage"] = 1
            advantage["advantage"] = 1
        elif btndisadvantage.state == "down" and btnhitadvantage.state == "normal" and btndamadvantage.state == "normal":
            advantage["hitadvantage"] = -1
            advantage["damadvantage"] = -1
            advantage["advantage"] = -1
        elif btnadvantage.state == "normal" and btndisadvantage.state == "normal" and btnhitadvantage.state == "normal" and btndamadvantage.state == "normal":
            advantage["hitadvantage"] = 0
            advantage["damadvantage"] = 0
            advantage["damadvantage"] = 0

    def initiative(self):
        advantagecheck()
        initval = Player.rollinitiative.attack(adv = advantage["advantage"])
        if initval["To Hit"] == "Miss":
            initval["To Hit"] = 1 + Player.initmod
        else:
            initval["To Hit"] = initval["To Hit"] + Player.initmod
        lbl.text = str(initval["To Hit"]) + " Initiative"
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
    

    def attackclick(self):
        advantagecheck()
        global crit
        attackval = Player.rollattack.attack(adv = advantage["advantage"], mod = tohitmod)
        lbl.text = str(attackval["To Hit"])+" Attack"
        crit = attackval["Critical"]
        if crit == True:
            lbl.text = (str(attackval["To Hit"]))+" Critical!" +" Attack"
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"

    def spellattackclick(self):
        advantagecheck()
        global crit
        attackval = Player.rollspellattack.attack(adv = advantage["advantage"])
        lbl.text = str(attackval["To Hit"])+" Attack"
        crit = attackval["Critical"]
        if crit == True:
            lbl.text = (str(attackval["To Hit"]))+" Critical!" +" Attack"
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"

    def damagecheck(damageval):
        global damage
        damage.append(damageval["Damage"])
        if attackval["Critical"] == True:
            lbl.text = "(Critical! To Hit " + str(attackval["To Hit"]) +  ") " + " (Damage " + str(sum(damage)) + ")"
        else:
            lbl.text = "(To Hit " + str(attackval["To Hit"]) + ") " + " (Damage " + str(sum(damage)) + ")"
        lbldamage.text = str(damage[::-1][0:8][::-1])
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"

    def action_1(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[0].dice > 0 or actions[0].damagemod > 0:
            if actions[0].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[0].tohit, adv = advantage["hitadvantage"], mod = actions[0].hitmod, improvedcrit = actions[0].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[0].tohit == 0:
                damageval = actions[0].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[0].bruteforce, brutalcrit = actions[0].brutalcrit, devastatingcrit = actions[0].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[0].ammunition > 0:
            actions[0].ammunition -= 1
            btnaction1.text = actions[0].name + " x " + str(actions[0].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
            
    def action_2(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[1].dice > 0 or actions[1].damagemod > 0:
            if actions[1].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[1].tohit,adv = advantage["hitadvantage"], mod = actions[1].hitmod, improvedcrit = actions[1].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[1].tohit == 0:
                damageval = actions[1].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[1].bruteforce,  brutalcrit = actions[1].brutalcrit, devastatingcrit = actions[1].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[1].ammunition > 0:
            actions[1].ammunition -= 1
            btnaction2.text = actions[1].name + " x " + str(actions[1].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_3(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[2].dice > 0 or actions[2].damagemod > 0:
            if actions[2].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[2].tohit, adv = advantage["hitadvantage"], mod = actions[2].hitmod, improvedcrit = actions[2].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[2].tohit == 0:
                damageval = actions[2].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[2].bruteforce,  brutalcrit = actions[2].brutalcrit, devastatingcrit = actions[2].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[2].ammunition > 0:
            actions[2].ammunition -= 1
            btnaction3.text = actions[2].name + " x " + str(actions[2].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_4(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[3].dice > 0 or actions[3].damagemod > 0:
            if actions[3].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[3].tohit, adv = advantage["hitadvantage"], mod = actions[3].hitmod, improvedcrit = actions[3].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[3].tohit == 0:
                damageval = actions[3].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[3].bruteforce,  brutalcrit = actions[3].brutalcrit, devastatingcrit = actions[3].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[3].ammunition > 0:
            actions[3].ammunition -= 1
            btnaction4.text = actions[3].name + " x " + str(actions[3].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_5(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[4].dice > 0 or actions[4].damagemod > 0:
            if actions[4].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[4].tohit, adv = advantage["hitadvantage"], mod = actions[4].hitmod, improvedcrit = actions[4].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[4].tohit == 0:
                damageval = actions[4].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[4].bruteforce,  brutalcrit = actions[4].brutalcrit, devastatingcrit = actions[4].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[4].ammunition > 0:
            actions[4].ammunition -= 1
            btnaction5.text = actions[4].name + " x " + str(actions[4].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_6(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[5].dice > 0 or actions[5].damagemod > 0:
            if actions[5].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[5].tohit, adv = advantage["hitadvantage"], mod = actions[5].hitmod, improvedcrit = actions[5].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[5].tohit == 0:
                damageval = actions[5].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[5].bruteforce,  brutalcrit = actions[5].brutalcrit, devastatingcrit = actions[5].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[5].ammunition > 0:
            actions[5].ammunition -= 1
            btnaction6.text = actions[5].name + " x " + str(actions[5].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_7(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[6].dice > 0 or actions[6].damagemod > 0:
            if actions[6].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[6].tohit, adv = advantage["hitadvantage"], mod = actions[6].hitmod, improvedcrit = actions[6].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[6].tohit == 0:
                damageval = actions[6].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[6].bruteforce,  brutalcrit = actions[6].brutalcrit, devastatingcrit = actions[6].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[6].ammunition > 0:
            actions[6].ammunition -= 1
            btnaction7.text = actions[6].name + " x " + str(actions[6].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_8(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[7].dice > 0 or actions[7].damagemod > 0:
            if actions[7].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[7].tohit, adv = advantage["hitadvantage"], mod = actions[7].hitmod, improvedcrit = actions[7].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[7].tohit == 0:
                damageval = actions[7].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[7].bruteforce,  brutalcrit = actions[7].brutalcrit, devastatingcrit = actions[7].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[7].ammunition > 0:
            actions[7].ammunition -= 1
            btnaction8.text = actions[7].name + " x " + str(actions[7].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_9(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[8].dice > 0 or actions[8].damagemod > 0:
            if actions[8].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[8].tohit, adv = advantage["hitadvantage"], mod = actions[8].hitmod, improvedcrit = actions[8].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[8].tohit == 0:
                damageval = actions[8].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[8].bruteforce,  brutalcrit = actions[8].brutalcrit, devastatingcrit = actions[8].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[8].ammunition > 0:
            actions[8].ammunition -= 1
            btnaction9.text = actions[8].name + " x " + str(actions[8].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def action_10(self):
        global attackval
        global crit
        global damageval
        advantagecheck()
        if actions[9].dice > 0 or actions[9].damagemod > 0:
            if actions[9].tohit != 0:
                attackval = Player.rollattack.attack(sides = actions[9].tohit, adv = advantage["hitadvantage"], mod = actions[9].hitmod, improvedcrit = actions[9].improvedcrit)
                crit = attackval["Critical"]
            if (attackval["HitMiss"] == "hit" and attackval["To Hit"] >= enemyac) or actions[9].tohit == 0:
                damageval = actions[9].damage(crit = crit, adv = advantage["damadvantage"], bruteforce = actions[9].bruteforce,  brutalcrit = actions[9].brutalcrit, devastatingcrit = actions[9].devastatingcrit)
            else:
                damageval["Damage"] = 0
            damagecheck(damageval)
        if actions[9].ammunition > 0:
            actions[9].ammunition -= 1
            btnaction10.text = actions[9].name + " x " + str(actions[9].ammunition)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def clear(self):
        global attackval
        global damage
        global crit
        attackval = {"To Hit": 0, "HitMiss": "hit", "Critical": False}
        crit = False
        damage = []
        lbl.text = "0"
        lbldamage.text = "History "
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"

    def endturn(self):
        global attackval
        global damage
        global turn
        global crit
        attackval = {"To Hit": 0, "HitMiss": "hit", "Critical": False}
        crit = False
        damage = []
        turn += 1
        lbl.text = "0"
        btnendturn.text = "End Turn " + str(turn)
        lbldamage.text = "History "
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"
        
    def rewindturn(self):
        global attackval
        global damage
        global turn
        global crit
        attackval = {"To Hit": 0, "HitMiss": "hit", "Critical": False}
        crit = False
        damage = []
        if turn > 1:
            turn -= 1
        lbl.text = "0"
        btnendturn.text = "End Turn " + str(turn)
        lbldamage.text = "History "
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        btnhitadvantage.state = "normal"
        btndamadvantage.state = "normal"

        
    def display():
        while True:

            try:
                lblenemy.text = "Enemy " + "AC-" + str(enemyac)
                    
                if Player.currenthp == Player.health or Player.currenthp > Player.health:
                    lblchar.text = str(Player.name) +"   " + "HP-" + str(Player.currenthp) + " (" + str(Player.currenthp - Player.health) + " Temp)"
                else:
                    lblchar.text = str(Player.name) +"   " + "HP-" + str(Player.currenthp)

                if tohitmod != 0:
                    if tohitmod > 0:
                        btnattack.text = "Weapon Attack! " + "+" + str(tohitmod)
                        btnspellattack.text = "Spell Attack! " + "+" + str(tohitmod)
                    else:
                        btnattack.text = "Weapon Attack! " + str(tohitmod)
                        btnspellattack.text = "Spell Attack! " + str(tohitmod)

                if (btnadvantage.state == "down" and btnhitadvantage.state == "normal" and btndamadvantage.state == "normal") or (btnadvantage.state == "down" and btnhitadvantage.state == "down" and btndamadvantage.state == "down"):
                    btnadvantage.text = "Advantage All"

                if btnadvantage.state == "down" and btnhitadvantage.state == "down" and btndamadvantage.state == "normal":
                    btnadvantage.text = "Advantage To Hit"

                if btnadvantage.state == "down" and btnhitadvantage.state == "normal" and btndamadvantage.state == "down":
                    btnadvantage.text = "Advantage Damage"

                if btnadvantage.state == "normal":
                    btnadvantage.text = "Advantage"

                if (btndisadvantage.state == "down" and btnhitadvantage.state == "normal" and btndamadvantage.state == "normal") or (btndisadvantage.state == "down" and btnhitadvantage.state == "down" and btndamadvantage.state == "down"):
                    btndisadvantage.text = "Disadvantage All"

                if btndisadvantage.state == "down" and btnhitadvantage.state == "down" and btndamadvantage.state == "normal":
                    btndisadvantage.text = "Disadvantage To Hit"

                if btndisadvantage.state == "down" and btnhitadvantage.state == "normal" and btndamadvantage.state == "down":
                    btndisadvantage.text = "Disadvantage Damage"

                if btndisadvantage.state == "normal":
                    btndisadvantage.text = "Disadvantage"
                    
                if tohitmod == 0:
                    btnattack.text = "Weapon Attack!"
                    btnspellattack.text = "Spell Attack!"

                btnaction1.text = actions[0].name
                if actions[0].ammunition > 0:
                    btnaction1.text = actions[0].name + " x " + str(actions[0].ammunition)

                btnaction2.text = actions[1].name
                if actions[1].ammunition > 0:
                    btnaction2.text = actions[1].name + " x " + str(actions[1].ammunition)

                btnaction3.text = actions[2].name
                if actions[2].ammunition > 0:
                    btnaction3.text = actions[2].name + " x " + str(actions[2].ammunition)

                btnaction4.text = actions[3].name
                if actions[3].ammunition > 0:
                    btnaction4.text = actions[3].name + " x " + str(actions[3].ammunition)

                btnaction5.text = actions[4].name
                if actions[4].ammunition > 0:
                    btnaction5.text = actions[4].name + " x " + str(actions[4].ammunition)

                btnaction6.text = actions[5].name
                if actions[5].ammunition > 0:
                    btnaction6.text = actions[5].name + " x " + str(actions[5].ammunition)

                btnaction7.text = actions[6].name
                if actions[6].ammunition > 0:
                    btnaction7.text = actions[6].name + " x " + str(actions[6].ammunition)

                btnaction8.text = actions[7].name
                if actions[7].ammunition > 0:
                    btnaction8.text = actions[7].name + " x " + str(actions[7].ammunition)

                btnaction9.text = actions[8].name
                if actions[8].ammunition > 0:
                    btnaction9.text = actions[8].name + " x " + str(actions[8].ammunition)

                btnaction10.text = actions[9].name
                if actions[9].ammunition > 0:
                    btnaction10.text = actions[9].name + " x " + str(actions[9].ammunition)

            except Exception as e:
                print (e)
                pass
            time.sleep(.125)

    def quitapp(self):
        Window.close()
        App.get_running_app().stop()

    btnsave = Button(text = "Quick Save")
    btnsave.bind(on_press = save_char)
    
    btnadvantage = ToggleButton(text="Advantage", group="advantage", state="normal")
    btndisadvantage = ToggleButton(text="Disadvantage", group="advantage", state="normal")    

    btninitiative = Button(text = "Initiative")
    btninitiative.bind(on_press = initiative)

    btnhealthup = Button(text = "+HP")
    btnhealthup.bind(on_press = charhealthup)

    btnhealthdn = Button(text = "-HP")
    btnhealthdn.bind(on_press = charhealthdn)

    btntohitdn = Button(text = "- To Hit")
    btntohitdn.bind(on_press = decreasehitmod)
    
    btntohitup = Button(text = "+ To Hit")
    btntohitup.bind (on_press = increasehitmod)

    btnheal = Button(text = "Heal")
    btnheal.bind(on_press = heal)

    btnenemyacup = Button(text = "+ Enemy AC")
    btnenemyacup.bind(on_press = enemyacup)

    btnenemyacdn = Button(text = "- Enemy AC")
    btnenemyacdn.bind(on_press = enemyacdn)

    btnattack = Button(text = "Weapon Attack!")
    btnattack.bind(on_press = attackclick)

    btnspellattack = Button(text = "Spell Attack!")
    btnspellattack.bind(on_press = spellattackclick)

    btnhitadvantage = ToggleButton(text="Adv/Disadv To Hit", group="hitadvantage", state="normal")
    btnhitdisadvantage = ToggleButton(text="Disadvantage To Hit", group="advantage", state="normal")
    btndamadvantage = ToggleButton(text="Adv/Disadv on Damage", group="damadvantage", state="normal")

    btnaction1 = Button(text = actions[0].name)
    if actions[0].ammunition > 0:
        btnaction1.text = actions[0].name + " X " + str(actions[0].ammunition)
    btnaction1.bind(on_press = action_1)

    btnaction2 = Button(text = actions[1].name)
    if actions[1].ammunition > 0:
        btnaction2.text = actions[1].name + " X " + str(actions[1].ammunition)
    btnaction2.bind(on_press = action_2)

    btnaction3 = Button(text = actions[2].name)
    if actions[2].ammunition > 0:
        btnaction3.text = actions[2].name + " X " + str(actions[2].ammunition)
    btnaction3.bind(on_press = action_3)

    btnaction4 = Button(text = actions[3].name)
    if actions[3].ammunition > 0:
        btnaction4.text = actions[3].name + " X " + str(actions[3].ammunition)
    btnaction4.bind(on_press = action_4)

    btnaction5 = Button(text = actions[4].name)
    if actions[4].ammunition > 0:
        btnaction5.text = actions[4].name + " X " + str(actions[4].ammunition)
    btnaction5.bind(on_press = action_5)

    btnaction6 = Button(text = actions[5].name)
    if actions[5].ammunition > 0:
        btnaction6.text = actions[5].name + " X " + str(actions[5].ammunition)
    btnaction6.bind(on_press = action_6)

    btnaction7 = Button(text = actions[6].name)
    if actions[6].ammunition > 0:
        btnaction7.text = actions[6].name + " X " + str(actions[6].ammunition)
    btnaction7.bind(on_press = action_7)

    btnaction8 = Button(text = actions[7].name)
    if actions[7].ammunition > 0:
        btnaction8.text = actions[7].name + " X " + str(actions[7].ammunition)
    btnaction8.bind(on_press = action_8)

    btnaction9 = Button(text = actions[8].name)
    if actions[8].ammunition > 0:
        btnaction9.text = actions[8].name + " X " + str(actions[8].ammunition)
    btnaction9.bind(on_press = action_9)

    btnaction10 = Button(text = actions[9].name)
    if actions[9].ammunition > 0:
        btnaction10.text = actions[9].name + " X " + str(actions[9].ammunition)
    btnaction10.bind(on_press = action_10)

    btnclear = Button(text = "Clear Rolls")
    btnclear.bind(on_press = clear)

    btnendturn = Button(text = "End Turn " + str(turn))
    btnendturn.bind(on_press = endturn)

    btnrewindturn = Button(text = "Rewind Turn")
    btnrewindturn.bind(on_press = rewindturn)

    btnquit = Button(text = "Quit")
    btnquit.bind(on_press = quitapp)

    statthread = threading.Thread(target = display)
    statthread.setDaemon(True)
    statthread.start()

    layout.add_widget(lblchar)
    layout.add_widget(lblenemy)
    layout.add_widget(btnenemyacdn)
    layout.add_widget(btnenemyacup)
    layout.add_widget(btnhealthdn)
    layout.add_widget(btnhealthup)
    layout.add_widget(lbl)
    layout.add_widget(lbldamage)
    layout.add_widget(btnadvantage)
    layout.add_widget(btndisadvantage)
    layout.add_widget(btnhitadvantage)
    layout.add_widget(btndamadvantage)
    layout.add_widget(btnheal)
    layout.add_widget(btninitiative)  
    layout.add_widget(btnaction1)
    layout.add_widget(btnaction2)
    layout.add_widget(btnaction3) 
    layout.add_widget(btnaction4)
    layout.add_widget(btnaction5)
    layout.add_widget(btnaction6)
    layout.add_widget(btnaction7)
    layout.add_widget(btnaction8)
    layout.add_widget(btnaction9)
    layout.add_widget(btnaction10)        
    layout.add_widget(btnclear)
    layout.add_widget(btnendturn)
    layout.add_widget(btnrewindturn)
    layout.add_widget(btnsave)
    return layout

class PlayerTabApp(App):

    def build(self):
        return PlayerTab()

"""
Checks Section
"""

def ChecksTab():
    layout = GridLayout(cols=2)
    lbl = Label(text= "0")
    lbldamage = Label(text= "History")

    btnadvantage = ToggleButton(text="Advantage", group="advantage", state="normal")
    btndisadvantage = ToggleButton(text="Disadvantage", group="advantage", state="normal")    

    def advantagecheck():
        global advantage
        if btnadvantage.state == "down":
            advantage["advantage"] = 1
        elif btndisadvantage.state == "down":
            advantage["advantage"] = -1
        else:
            advantage["advantage"] = 0
    
    def damagecheck(damageval):
        global checkhistory
        checkhistory.append(damageval["Damage"])
        lbl.text = str(checkhistory[-1])
        lbldamage.text = str(checkhistory[::-1][0:8][::-1])
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        
    def clear(self):
        global checkhistory
        checkhistory = []
        lbl.text = "0"
        lbldamage.text = "History "
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"

    def acrobaticscheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.acrobatics, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def animalhandlingcheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.animalhandling, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def arcanacheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.arcana, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def athleticscheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.athletics, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def deceptioncheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.deception, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def historycheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.history, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def insightcheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.insight, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def intimidationcheck(self):
        advantagecheck()
        roller = Roller(20, 1,dammod = Player.intimidation, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def investigationcheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.investigation, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def medicinecheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.medicine, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def naturecheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.nature, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def perceptioncheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.perception, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def performancecheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.performance, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def persuasioncheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.persuasion, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def religioncheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.religion, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def sleightofhandcheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.sleightofhand, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def stealthcheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.stealth, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def survivalcheck(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.survival, crit = crit, adv = advantage["advantage"])
        roll =  roller.damage(crit, advantage["advantage"])
        damagecheck(roll)
        
    btnacrobatics = Button(text = "Acrobatics")
    btnacrobatics.bind(on_press = acrobaticscheck)

    btnanimalhandling = Button(text = "Animal Handling")
    btnanimalhandling.bind(on_press = animalhandlingcheck)

    btnarcana = Button(text = "Arcana")
    btnarcana.bind(on_press = arcanacheck)

    btnathletics = Button(text = "Athletics")
    btnathletics.bind(on_press = athleticscheck)

    btndeception = Button(text = "Deception")
    btndeception.bind(on_press = deceptioncheck)

    btnhistory = Button(text = "History")
    btnhistory.bind(on_press = historycheck)

    btninsight = Button(text = "Insight")
    btninsight.bind(on_press = insightcheck)

    btnintimidation = Button(text = "Intimidation")
    btnintimidation.bind(on_press = intimidationcheck)

    btninvestigation = Button(text = "Investigation")
    btninvestigation.bind(on_press = investigationcheck)

    btnmedicine = Button(text = "Medicine")
    btnmedicine.bind(on_press = medicinecheck)

    btnnature = Button(text = "Nature")
    btnnature.bind(on_press = naturecheck)

    btnperception = Button(text = "Perception")
    btnperception.bind(on_press = perceptioncheck)

    btnperformance = Button(text = "Performance")
    btnperformance.bind(on_press = performancecheck)

    btnpersuasion = Button(text = "Persuasion")
    btnpersuasion.bind(on_press = persuasioncheck)

    btnreligion = Button(text = "Religion")
    btnreligion.bind(on_press = religioncheck)

    btnsleightofhand = Button(text = "Sleight of Hand")
    btnsleightofhand.bind(on_press = sleightofhandcheck)

    btnstealth = Button(text = "Stealth")
    btnstealth.bind(on_press = stealthcheck)

    btnsurvival = Button(text = "Survival")
    btnsurvival.bind(on_press = survivalcheck)

    btnclear = Button(text = "Clear Rolls")
    btnclear.bind(on_press = clear)

    layout.add_widget(lbl)
    layout.add_widget(lbldamage)
    layout.add_widget(btnadvantage)
    layout.add_widget(btndisadvantage)
    layout.add_widget(btnacrobatics)
    layout.add_widget(btnanimalhandling)
    layout.add_widget(btnarcana)
    layout.add_widget(btnathletics)
    layout.add_widget(btndeception)
    layout.add_widget(btnhistory)
    layout.add_widget(btninsight)
    layout.add_widget(btnintimidation)
    layout.add_widget(btninvestigation)
    layout.add_widget(btnmedicine)
    layout.add_widget(btnnature)
    layout.add_widget(btnperception)
    layout.add_widget(btnperformance)
    layout.add_widget(btnpersuasion)
    layout.add_widget(btnreligion)
    layout.add_widget(btnsleightofhand)
    layout.add_widget(btnstealth)
    layout.add_widget(btnsurvival)
    layout.add_widget(btnclear)

    return layout

class ChecksTabApp(App):

    def build(self):
        return ChecksTab()

"""
Saves Section
"""

def SavesTab():
    layout = GridLayout(cols=2)
    lbl = Label(text= "0")
    lbldamage = Label(text= "History")

    btnadvantage = ToggleButton(text="Advantage", group="advantage", state="normal")
    btndisadvantage = ToggleButton(text="Disadvantage", group="advantage", state="normal")    

    def advantagecheck():
        global advantage
        if btnadvantage.state == "down":
            advantage["advantage"] = 1
        elif btndisadvantage.state == "down":
            advantage["advantage"] = -1
        else:
            advantage["advantage"] = 0
    
    def damagecheck(damageval):
        global savehistory
        savehistory.append(damageval["Damage"])
        lbl.text = str(savehistory[-1])
        lbldamage.text = str(savehistory[::-1][0:8][::-1])
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        
    def clear(self):
        global savehistory
        savehistory = []
        lbl.text = "0"
        lbldamage.text = "History"
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"

    def strengthsave(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.strsave)
        roll = roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def dexteritysave(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.dexsave)
        roll = roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def constitutionsave(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.consave)
        roll = roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def intelligencesave(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.intsave)
        roll = roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def wisdomsave(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.wissave)
        roll = roller.damage(crit, advantage["advantage"])
        damagecheck(roll)

    def charismasave(self):
        advantagecheck()
        roller = Roller(20, 1, dammod = Player.chasave)
        roll = roller.damage(crit, advantage["advantage"])
        damagecheck(roll)
        
    btnstrengthsave = Button(text = "Strength")
    btnstrengthsave.bind(on_press = strengthsave)

    btndexteritysave = Button(text = "Dexterity")
    btndexteritysave.bind(on_press = dexteritysave)

    btnconstitutionsave = Button(text = "Constitution")
    btnconstitutionsave.bind(on_press = constitutionsave)

    btnintelligencesave = Button(text = "Intelligence")
    btnintelligencesave.bind(on_press = intelligencesave)

    btnwisdomsave = Button(text = "Wisdom")
    btnwisdomsave.bind(on_press = wisdomsave)

    btncharismasave = Button(text = "Charisma")
    btncharismasave.bind(on_press = charismasave)


    btnclear = Button(text = "Clear Rolls")
    btnclear.bind(on_press = clear)

    layout.add_widget(lbl)
    layout.add_widget(lbldamage)
    layout.add_widget(btnadvantage)
    layout.add_widget(btndisadvantage)
    layout.add_widget(btnstrengthsave)
    layout.add_widget(btndexteritysave)
    layout.add_widget(btnconstitutionsave)
    layout.add_widget(btnintelligencesave)
    layout.add_widget(btnwisdomsave)
    layout.add_widget(btncharismasave)
    layout.add_widget(btnclear)

    return layout

class SavesTabApp(App):

    def build(self):
        return SavesTab()

"""
Character Section
"""

characters = []
try:
    if len(filelist) > 0:
        for i in filelist:
            if i[::-1][0:3].lower() == "txt":
                tempchar = i[::-1]
                tempchar = tempchar[4:]
                characters.append(tempchar[::-1])
except:
    pass

statplace = 0
charcount = 0

def CharacterTab():
    layout = GridLayout(cols=2)
    lbl = Label(text= "Attribute Value")
    lblblank = Label(text="")
    lblname = Label(text="Character")
    nameinput = TextInput(text=Player.name, multiline=False)
    lbltitle = Label(text= "Attribute")

    def statup(self):
        global statplace
        statplace += 1
        if statplace == len(charstatlist):
            statplace = 0
        if charstatlist[statplace] == "Health":
            lbltitle.text = "MaxHP"
        else:
            lbltitle.text = charstatlist[statplace]
        lbl.text = str(getattr(Player,charstatlist[statplace].lower()))

    def statdn(self):
        global statplace
        statplace -= 1
        if statplace < 0:
            statplace = (len(charstatlist) -1)
        if charstatlist[statplace] == "Health":
            lbltitle.text = "MaxHP"
        else:
            lbltitle.text = charstatlist[statplace]
        lbl.text = str(getattr(Player,charstatlist[statplace].lower()))
        
    def clear(self):
        lbl.text = "0"
        setattr(Player,charstatlist[statplace].lower(),int(lbl.text))
            
    def add(self):
        try:
            if lbl.text != str(Player.name):
                lbl.text = str(int(lbl.text) + 1)
                setattr(Player,charstatlist[statplace].lower(),int(lbl.text))
        except Exception as e:
            print(e)
        
    def subtract(self):
        try:
            if lbl.text != str(Player.name):
                lbl.text = str(int(lbl.text) - 1)
                setattr(Player,charstatlist[statplace].lower(),int(lbl.text))
        except Exception as e:
            print(e)

    def charup(self):
        global charcount
        global characters
        try:
            if len(characters) > 1:
                charcount += 1
            if charcount == len(characters):
                charcount = 0
            nameinput.text = characters[charcount]
        except:
            pass

    def chardn(self):
        global charcount
        global characters
        try:
            charcount -= 1
            if charcount < 0:
                charcount = len(characters) - 1
            nameinput.text = characters[charcount]
        except:
            pass

    def setchar(self):
        global Player
        global actions

        try:
            with open(savepath + str(nameinput.text) + ".txt") as charfile:
                    characterfile = json.load(charfile)
            savefile = savepath + str(nameinput.text) + ".txt"
        
            if nameinput.text in characters:
                Player = Character(characterfile)
                actions = defineactions(characterfile)

        except Exception as e:
            print(e)
            

    def savecharacter(self):
        global characters
        savefile = savepath + str(nameinput.text) + ".txt"
        
        if nameinput.text[::-1][0:9] == ")deteleD(" or nameinput.text == "Invalid Name, Try Again":
            nameinput.text = "Invalid Name, Try Again"
        else:
            if nameinput.text not in characters:
                characters.append(nameinput.text)
            save(name = str(nameinput.text), savefile = savefile)

        setchar(self)

    def deletechar(self):
        global characters
        global charcount
        tempname = nameinput.text
        deleted = " (Deleted)"
        try:
            os.remove(savepath + nameinput.text + ".txt")
            nameinput.text = nameinput.text + deleted
            if nameinput.text[::-1][0:9] != deleted[::-1]:
                del characters[charcount]
                charcount -= 1
            
        except:
            pass

        

    lblblank1 = Label(text = "")
    lblblank2 = Label(text = "")

    btnadd =  Button(text = "+")
    btnadd.bind(on_press = add)

    btnsubtract = Button(text = "-")
    btnsubtract.bind(on_press = subtract)

    btnprvchar = Button(text = "Previous Character")
    btnprvchar.bind(on_press = chardn)
    
    btnnxtchar = Button(text = "Next Character")
    btnnxtchar.bind(on_press = charup)

    btnnext = Button(text = "Next Attribute")
    btnnext.bind(on_press = statup)

    btnprev = Button(text = "Previous Attribute")
    btnprev.bind(on_press = statdn)

    btnset = Button(text = "Load Character")
    btnset.bind(on_press = setchar)
    
    btnsave = Button(text = "Save Character")
    btnsave.bind(on_press = savecharacter)
    
    btndelete = Button(text = "Delete Character")
    btndelete.bind(on_press = deletechar)

    btnclear = Button(text = "Clear Value")
    btnclear.bind(on_press = clear)

    layout.add_widget(lblname)
    layout.add_widget(nameinput)
    layout.add_widget(lbltitle)
    layout.add_widget(lbl)
    layout.add_widget(btnsubtract)
    layout.add_widget(btnadd)
    layout.add_widget(btnprev)
    layout.add_widget(btnnext)
    layout.add_widget(btnprvchar)
    layout.add_widget(btnnxtchar)
    layout.add_widget(btnset)
    layout.add_widget(btnsave)
    layout.add_widget(btndelete)
    layout.add_widget(btnclear)
    layout.add_widget(lblblank1)
    layout.add_widget(lblblank2)

    return layout

class CharacterTabApp(App):

    def build(self):
        return CharacterTab()


"""
Actions Section
"""

actionplace = 0
statplace = 0

def ActionsTab():
    layout = GridLayout(cols=2)
    lbl = Label(text= "Attribute Value")
    lblname = Label(text="Action Name")
    lblblank = Label(text="")
    lbltitle = Label(text= "Action Attribute")
    lblaction = Label(text="Action")
    nameinput = TextInput(text=actions[0].name, multiline=False)

    def attribup(self):
        global statplace
        global actionattrib
        statplace += 1
        if statplace == len(actionattrib):
            statplace = 0
            lbltitle.text = actionattrib[statplace]
        else:
            lbltitle.text = actionattrib[statplace]
        lbl.text = str(getattr(actions[actionplace],actionattrib[statplace].lower()))

    def attribdn(self):
        global statplace
        global actionattib
        statplace -= 1
        if statplace < 0:
            statplace = (len(actionattrib) -1)
            lbltitle.text = actionattrib[statplace]
        else:
            lbltitle.text = actionattrib[statplace]
        lbl.text = str(getattr(actions[actionplace],actionattrib[statplace].lower()))
        
    def clear(self):
        lbl.text = "0"
        setattr(Player,charstatlist[statplace].lower(),int(lbl.text))
            
    def add(self):
        try:
            lbl.text = str(int(lbl.text) + 1)
            setattr(actions[actionplace],actionattrib[statplace].lower(),int(lbl.text))
        except:
            pass

    def subtract(self):
        try:
            lbl.text = str(int(lbl.text) - 1)
            setattr(actions[actionplace],actionattrib[statplace].lower(),int(lbl.text))
        except:
            pass

    def actionup(self):
        global actionplace
        global actions
        if len(actions) > 1:
            actionplace += 1
        if actionplace == len(actions):
            actionplace = 0
        nameinput.text = str(actions[actionplace].name)

    def actiondn(self):
        global actionplace
        global actions
        actionplace -= 1
        if actionplace < 0:
            actionplace = len(actions) - 1
        nameinput.text = str(actions[actionplace].name)

    def nameaction(self):
        global actionplace
        actions[actionplace].name = str(nameinput.text)

        

    lblblank1 = Label(text = "")
    lblblank2 = Label(text = "")

    btnadd =  Button(text = "+")
    btnadd.bind(on_press = add)

    btnsubtract = Button(text = "-")
    btnsubtract.bind(on_press = subtract)

    btnprvaction = Button(text = "Previous Action")
    btnprvaction.bind(on_press = actiondn)
    
    btnnxtaction = Button(text = "Next Action")
    btnnxtaction.bind(on_press = actionup)

    btnnext = Button(text = "Next Attribute")
    btnnext.bind(on_press = attribup)

    btnprev = Button(text = "Previous Attribute")
    btnprev.bind(on_press = attribdn)
    
    btnname = Button(text = "Set Action Name")
    btnname.bind(on_press = nameaction)

    btnclear = Button(text = "Clear Value")
    btnclear.bind(on_press = clear)

    layout.add_widget(lblname)
    layout.add_widget(nameinput)
    layout.add_widget(lbltitle)
    layout.add_widget(lbl)
    layout.add_widget(btnsubtract)
    layout.add_widget(btnadd)
    layout.add_widget(btnprev)
    layout.add_widget(btnnext)
    layout.add_widget(btnprvaction)
    layout.add_widget(btnnxtaction)
    layout.add_widget(btnname)
    layout.add_widget(btnclear)
    layout.add_widget(lblblank1)
    layout.add_widget(lblblank2)

    return layout

class ActionsTabApp(App):

    def build(self):
        return CharacterTab()

"""
Basic Roller Section
"""

def BasicRollerTab():
    layout = GridLayout(cols=2)
    lbl = Label(text= "0")
    lblblank = Label(text= "")
    lbldamage = Label(text= "History")

    lbldice = Label(text = "Dice " + str(dice))
    lblmodifier = Label(text = "Modifier " + str(modifier))
    lblmultiplier = Label(text = "Multiplier " + str(multiplier))

    btnadvantage = ToggleButton(text="Advantage", group="advantage", state="normal")
    btndisadvantage = ToggleButton(text="Disadvantage", group="advantage", state="normal")    

    def advantagecheck():
        global advantage
        if btnadvantage.state == "down":
            advantage["advantage"] = 1
        elif btndisadvantage.state == "down":
            advantage["advantage"] = -1
        else:
            advantage["advantage"] = 0
    
    def damagecheck(roll):
        advantagecheck()
        global simplehistory
        rolled = roll.damage(adv = advantage["advantage"])
        simplehistory.append(rolled["Damage"])
        lbl.text = str(simplehistory[-1])
        lbldamage.text = str(simplehistory[::-1][0:8][::-1])
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
        
    def clear(self):
        global simplehistory
        global modifier
        global multiplier
        global dice
        simplehistory = []
        lbl.text = "0"
        lbldamage.text = str(simplehistory)
        btnadvantage.state = "normal"
        btndisadvantage.state = "normal"
    
    def d4(self):
        roll = Roller(4, dice, 0, (modifier * multiplier))
        damagecheck(roll)

    def d6(self):
        roll = Roller(6, dice, 0, (modifier * multiplier))
        damagecheck(roll)
        
    def d8(self):
        roll = Roller(8, dice, 0, (modifier * multiplier))
        damagecheck(roll)
        
    def d10(self):
        roll = Roller(10, dice, 0, (modifier * multiplier))
        damagecheck(roll)
        
    def d12(self):
        roll = Roller(12, dice, 0, (modifier * multiplier))
        damagecheck(roll)
        
    def d20(self):
        roll = Roller(20, dice, 0, (modifier * multiplier))
        damagecheck(roll)
        
    def d100(self):
        roll = Roller(100, dice, 0, (modifier * multiplier))
        damagecheck(roll)
        
    def diceup(self):
        global dice
        dice += 1
        lbldice.text = "Dice " + str(dice)

    def dicedn(self):
        global dice
        dice -= 1
        if dice < 1:
            dice = 1
        lbldice.text = "Dice " + str(dice)

    def modup(self):
        global modifier
        modifier += 1
        lblmodifier.text = "Modifier " + str(modifier)

    def moddn(self):
        global modifier
        modifier -= 1
        lblmodifier.text = "Modifier " + str(modifier)

    def multup(self):
        global multiplier
        multiplier += 1
        lblmultiplier.text = "Multiplier " + str(multiplier)

    def multdn(self):
        global multiplier
        multiplier -= 1
        if multiplier < 1:
            multiplier = 1
        lblmultiplier.text = "Multiplier " + str(multiplier)

    btndiceup =  Button(text = "+ Dice")
    btndiceup.bind(on_press = diceup)

    btndicedn = Button(text = "- Dice")
    btndicedn.bind(on_press = dicedn)

    btnmodup = Button(text = "+ Modifier")
    btnmodup.bind(on_press = modup)

    btnmoddn = Button(text = "- Modifier")
    btnmoddn.bind(on_press = moddn)

    btnmultup = Button(text = "+ Multiplier")
    btnmultup.bind(on_press = multup)

    btnmultdn = Button(text = "- Multiplier")
    btnmultdn.bind(on_press = multdn)
        
    btnd4 = Button(text = "D4")
    btnd4.bind(on_press = d4)

    btnd6 = Button(text = "D6")
    btnd6.bind(on_press = d6)

    btnd8 = Button(text = "D8")
    btnd8.bind(on_press = d8)

    btnd10 = Button(text = "D10")
    btnd10.bind(on_press = d10)

    btnd12 = Button(text = "D12")
    btnd12.bind(on_press = d12)

    btnd20 = Button(text = "D20")
    btnd20.bind(on_press = d20)

    btnd100 = Button(text = "D100")
    btnd100.bind(on_press = d100)

    btnclear = Button(text = "Clear Rolls")
    btnclear.bind(on_press = clear)

    layout.add_widget(lbl)
    layout.add_widget(lbldamage)
    layout.add_widget(lblblank)
    layout.add_widget(lbldice)
    layout.add_widget(lblmodifier)
    layout.add_widget(lblmultiplier)
    layout.add_widget(btndicedn)
    layout.add_widget(btndiceup)
    layout.add_widget(btnmoddn)
    layout.add_widget(btnmodup)
    layout.add_widget(btnmultdn)
    layout.add_widget(btnmultup)
    layout.add_widget(btnadvantage)
    layout.add_widget(btndisadvantage)
    layout.add_widget(btnd4)
    layout.add_widget(btnd6)
    layout.add_widget(btnd8)
    layout.add_widget(btnd10)
    layout.add_widget(btnd12)
    layout.add_widget(btnd20)
    layout.add_widget(btnd100)
    layout.add_widget(btnclear)

    return layout

class BasicRollerTabApp(App):

    def build(self):
        return BasicRollerTab()

"""
Main GUI Section
"""

def TabbedScreen():
    tp = TabbedPanel()
##    tp.background_image = "Icon.png"
    tp.do_default_tab = False
    th = TabbedPanelHeader(text='Combat')
    th2 = TabbedPanelHeader(text='Checks')
    th3 = TabbedPanelHeader(text='Saves')
    th4 = TabbedPanelHeader(text='Roller')
    th5 = TabbedPanelHeader(text="Character")
    th6 = TabbedPanelHeader(text="Actions")
    tp.add_widget(th)
    tp.add_widget(th2)
    tp.add_widget(th3)
    tp.add_widget(th4)
    tp.add_widget(th5)
    tp.add_widget(th6)

    th.content = PlayerTab()
    th2.content = ChecksTab()
    th3.content = SavesTab()
    th4.content = BasicRollerTab()
    th5.content = CharacterTab()
    th6.content = ActionsTab()
    return tp

class CombatRoller(App):

    def build(self):

        Window.bind(on_keyboard=self.key_input)
        return TabbedScreen()

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            self.root_window.close()
            App.get_running_app().stop()
        else:
            return False


if __name__ == "__main__":

    CombatRoller().run()
