#!/usr/bin/env python
# -*- coding: utf8 -*-
#importing and exporting csv files
import csv
#for using round function in calculating health
import math
#for copy.deepcopy() to properly copy lists without pointers
import copy


'''
Things you must add/change when implementing a new patch

1. Generate a new csv file of the newest patch with all of the stats (recommend to just take the newest patch and modify it)
2. Backtrack all of these changes you made from the patch for the appropriate hero
3. Add new patch in patch list.
4. Update buff/nerf csv table that is to be imported into this database (might be a little more complicated than simple adding a column)
'''


'''
A patch will contain a patch_num identifier and a list of heroes.
'''
class Patch:
    def __init__(self, patch_num):
        self.patch_num = patch_num
        self.heroes = []

'''
A hero class contains a dictionary of attributes. The __init__ function is to make sure a hero is created with all of the attributes. The __str__ function
is to properly print out all of the attributes of the hero (used for debugging). The __iter__ function is for setting an order for the attributes to be iterated
through when exporting to csv.
'''

class Hero:

    def __init__(self, hero_id, nerf_buff, attribute, strength, intelligence, agility, str_gain, intel_gain, agi_gain, attack_range, base_attack_time,
    movement_speed, armor, damage_lower, damage_upper, missile_speed, cast_duration_before, cast_duration_after, hp_regen, mp_regen, magic_res,
    day_vision, night_vision, turn_rate):
        self.hero_id = hero_id
        self.nerf_buff = nerf_buff
        self.attribute = attribute
        self.strength = float(strength)
        self.intelligence = float(intelligence)
        self.agility = float(agility)
        self.str_gain = float(str_gain)
        self.intel_gain = float(intel_gain)
        self.agi_gain = float(agi_gain)
        self.attack_range = float(attack_range)
        self.base_attack_time = float(base_attack_time)
        self.movement_speed = float(movement_speed)
        self.armor = float(armor)
        self.damage_lower = float(damage_lower)
        self.damage_upper = float(damage_upper)
        self.missile_speed = float(missile_speed)
        self.cast_duration_before = float(cast_duration_before)
        self.cast_duration_after = float(cast_duration_after)
        self.hp_regen = float(hp_regen)
        self.mp_regen = float(mp_regen)
        self.magic_res = float(magic_res)
        self.day_vision = float(day_vision)
        self.night_vision = float(night_vision)
        self.turn_rate = turn_rate

        #calculated stuff
        self.damage_avg = (float(damage_lower) + float(damage_upper)) / 2
        self.str_25 = round(float(strength) + math.floor(float(str_gain)*24),2)
        self.int_25 = round(float(intelligence) + math.floor(float(intel_gain)*24),2)
        self.agi_25 = round(float(agility) + math.floor(float(agi_gain)*24),2)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __iter__(self):
        return iter([self.hero_id, self.nerf_buff, self.attribute, self.strength, self.intelligence, self.agility,
        self.str_gain, self.intel_gain, self.agi_gain, self.attack_range, self.base_attack_time, self.movement_speed,
        self.armor, self.damage_lower, self.damage_upper, self.missile_speed, self.cast_duration_before, self.cast_duration_after,
        self.hp_regen, self.mp_regen, self.magic_res, self.day_vision, self.night_vision, self.turn_rate, self.damage_avg,
        self.str_25, self.int_25, self.agi_25])
'''
This next section is changing an attribute for the patch. There are two things to take note when implementing a change to an attribute.
Firstly (this is more easily explained throught example): You must change the attribute for the patch before it was changed. Such as,
Abaddon has his movement speed raised by 5 in patch 7.18, so you would set the conditional to (patchNum == 7.17).
Secondly: Since the stats are copied from the newest patch, and each change is calculated by going backwards in time, each change is
inverted. Abaddon's movement speed is increased by 5 in patch 7.18 so we must remove 5 movement speed from abaddon as we go from patch 7.18 to
patch 7.17.
Thirdly: There are several changes (which are found in another section) that encompass a spectrum of heroes (eg all strength heroes). I added a way to
do this without changing every hero. I did not include a note in each case where it applies.
'''
 
def abaddon(patchNum, hero):
    if(patchNum == 7.19):
        hero.movement_speed = 310
        hero.agility = 17
    if(patchNum == 7.17):
        hero.movement_speed = hero.movement_speed - 5
    if(patchNum == 7.03):
        hero.str_gain = 2.5
    if(patchNum == 6.78):
        hero.armor = hero.armor + 1
    #if(patchNum == 7.12):
        #hero.movement_speed = hero.movement_speed + 5 #included in attribute cases
        #hero.armor = hero.armor + 1
    return hero
 
def alchemist(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed = hero.movement_speed - 10
        hero.agility = 16
    #if(patchNum == 7.12):
        #hero.movement_speed = hero.movement_speed + 5 #included in attribute cases
        #hero.armor = hero.armor + 1
    if(patchNum == 7.05):
        hero.agility = hero.agility - 5
    return hero
 
def axe(patchNum, hero):
    if(patchNum == 7.13):
        hero.movement_speed = hero.movement_speed - 5
    if(patchNum == 7.06):
        hero.hp_regen = hero.hp_regen - 2.75
    if(patchNum == 6.79):
        hero.hp_regen = hero.hp_regen - 1
    return hero
 
def beastmaster(patchNum, hero):
    if(patchNum == 7.16):
        hero.armor = hero.armor + 2
    if(patchNum == 6.83):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.8):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    return hero
 
def brewmaster(patchNum, hero):
    if(patchNum == 7.19):
        hero.intel_gain = 1.3
        hero.movement_speed = 295
    if(patchNum == 7.06):
        hero.hp_regen = 0.5
    if(patchNum == 6.82):
        hero.armor = 4
    if(patchNum == 6.78):
        hero.agility = 16
    return hero
 
def bristleback(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain =  2.2
    if(patchNum == 7.05):
        hero.str_gain = 2.5
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
    if(patchNum == 6.83):
        hero.movement_speed = 290
        hero.base_attack_time = 1.7
    if(patchNum == 6.79):
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
    return hero
 
def centaur(patchNum, hero):
    if(patchNum == 7.19):
        hero.str_gain = 4.3
    if(patchNum == 7.18):
        hero.strength = 25
    if(patchNum == 7.17):
        hero.strength = 23
    if(patchNum == 7.15):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 7.12):
        hero.movement_speed = 300
        hero.armor = 0
    if(patchNum == 7.06):
        hero.agi_gain = 1.6
    if(patchNum == 7.02):
        hero.armor = 1
    if(patchNum == 7):
        hero.agi_gain = 2
    return hero
 
def chaos_knight(patchNum , hero):
    if(patchNum == 7.15):
        hero.intelligence = hero.intelligence - 2
    if(patchNum == 7.05):
        hero.strength = 20
    return hero
 
def clockwerk(patchNum, hero):
    if(patchNum == 7.16):
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
    if(patchNum == 7.05):
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.04):
        hero.strength = 24
    if(patchNum == 6.85):
        hero.str_gain = 2.7
    return hero
 
def doom(patchNum, hero):
    if(patchNum == 7.19):
        hero.attack_range = 150
    if(patchNum == 7.17):
        hero.movement_speed = 285
    if(patchNum == 7.12):
        hero.armor = hero.armor - 1 #counteract 7.13 attribute case
    if(patchNum == 7.09):
        hero.intelligence = hero.intelligence - 2
    if(patchNum == 6.85):
        hero.base_attack_time = 1.7
    return hero
 
def dragon_knight(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 10
    if(patchNum == 7.15):
        hero.movement_speed = 285
    if(patchNum == 7.09):
        hero.agi_gain = 2.2
    if(patchNum == 6.86):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    return hero
 
def earth_spirit(patchNum, hero):
    if(patchNum == 7.19):
        hero.str_gain = 3.5
    if(patchNum == 7.17):
        hero.str_gain = 3.2
    if(patchNum == 7.02):
        hero.movement_speed = 295
    if(patchNum == 6.86):
        hero.movement_speed = 305
    if(patchNum == 6.85):
        hero.intel_gain = 2.4
    return hero
 
def earth_shaker(patchNum, hero):
    if(patchNum == 7.18):
        hero.armor = 1
    if(patchNum == 7.17):
        hero.hp_regen = 2
        hero.movement_speed = 305
    if(patchNum == 7.13):
        hero.armor = 0
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 6.8):
        hero.turn_rate = .6
    if(patchNum == 6.79):
        hero.movement_speed = 300
        hero.str_gain = 2.5
    return hero
 
def elder_titan(patchNum, hero):
    if(patchNum == 7.06):
        hero.turn_rate = .4
    if(patchNum == 7.02):
        hero.agi_gain = 1.5
    return hero
  
def huskar(patchNum, hero):
    if(patchNum == 7.18):
        hero.damage_upper = hero.damage_upper + 6
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 2
    if(patchNum == 7.06):
        hero.movement_speed = 300
    if(patchNum == 6.78):
        hero.agility = 20
        hero.agi_gain = 2.4
    return hero
 
def wisp(patchNum, hero):
    if(patchNum == 7.12):
        hero.armor = hero.armor - 1 #counteract 7.13 attribute case
    if(patchNum == 7.13):
        hero.movement_speed = 290
    if(patchNum == 7.12):
        hero.movement_speed = 295
    if(patchNum == 7.11):
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_avg = hero.damage_avg + 4
    return hero
 
def kunkka(patchNum, hero):
    if(patchNum == 6.86):
        hero.armor = 0
    return hero
 
def legion_commander(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 15
    if(patchNum == 6.84):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.78):
        hero.movement_speed = 310
    return hero
 
def lifestealer(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 3.6
        hero.armor -= 2
        hero.movement_speed -= 15
    if(patchNum == 7.19):
        hero.agi_gain = 1.9
    if(patchNum == 7.05):
        hero.str_gain = 3.3
    if(patchNum == 7.03):
        hero.damage_upper = hero.damage_upper + 2
        hero.damage_lower = hero.damage_lower + 2
        hero.damage_avg = hero.damage_avg + 2
    if(patchNum == 7.02):
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 6.87):
        hero.base_attack_time = 1.7
    if(patchNum == 6.86):
        hero.str_gain = 2.4
    return hero
 
def lycan(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain=3.8
        hero.armor -= 1
        hero.movement_speed -= 15
    if(patchNum == 7.12):
        hero.armor = hero.armor - 1 #counteract 7.13 attribute case
    if(patchNum == 7.17):
        hero.armor = hero.armor + 2
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.15):
        hero.intel_gain = 1.55
    if(patchNum == 7.09):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.07):
        hero.armor = hero.armor + 1
    if(patchNum == 7.03):
        hero.strength = hero.strength - 3
    if(patchNum == 7.01):
        hero.agi_gain = 1
    if(patchNum == 7):
        hero.agi_gain = 1.5
    if(patchNum == 6.84):
        hero.str_gain = 2.75
    if(patchNum == 6.78):
        hero.damage_lower = hero.damage_lower - 5
        hero.damage_upper = hero.damage_upper - 5
        hero.damage_avg = hero.damage_avg - 5
        hero.armor = hero.armor + 1
    return hero
 
def magnus(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 3.7
    if(patchNum == 7.16):
        hero.strength = hero.strength - 1
    if(patchNum == 7.09):
        hero.strength = hero.strength - 1
    if(patchNum == 7.06):
        hero.hp_regen = 0.5
    if(patchNum == 7.03):
        hero.base_attack_time = 1.7
    if(patchNum == 6.87):
        hero.hp_regen = 2.75
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.79):
        hero.intelligence = hero.intelligence - 2
    if(patchNum == 6.78):
        hero.turn_rate = 0.5
    return hero
 
def nightstalker(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 3.2
    if(patchNum == 7.17):
        hero.movement_speed = 290
    if(patchNum == 7.06):
        hero.hp_regen = 1.75
        hero.day_vision = 1200
    if(patchNum == 7.05):
        hero.intelligence = 16
    if(patchNum == 6.84):
        hero.hp_regen = 0.25
    if(patchNum == 6.82):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    return hero

def omniknight(patchNum, hero):
    if(patchNum == 7.13):
        hero.armor = 2
    if(patchNum == 7.12):
        hero.movement_speed = 300
        hero.armor = 3
    if(patchNum == 7.06):
        hero.intelligence = hero.intelligence + 2
    if(patchNum == 6.87):
        hero.strength = 20
        hero.str_gain = 2.65
    if(patchNum == 6.81):
        hero.armor = hero.armor - 1
    return hero

def phoenix(patchNum, hero):
    if(patchNum == 7.12):
        hero.armor = hero.armor - 1 #counteract 7.13 attribute case
    if(patchNum == 7.04):
        hero.strength = hero.strength - 2
    return hero
 
def pudge(patchNum, hero):
    if(patchNum == 7.20):
        hero.damage_upper -= 6
        hero.damage_lower -= 6
        hero.damage_avg -= 6
    if(patchNum == 7.13):
        hero.damage_upper = hero.damage_upper - 7
        hero.damage_lower = hero.damage_lower - 7
        hero.damage_avg = hero.damage_avg - 7
    if(patchNum == 7.01):
        hero.movement_speed = 285
    if(patchNum == 6.81):
        hero.turn_rate = 0.5
    return hero

def sand_king(patchNum, hero):
    if(patchNum == 7.20):
        hero.intelligence -= 3
    if(patchNum == 7.19):
        hero.damage_upper += 2
        hero.damage_lower += 2
        hero.damage_avg += 2
    if(patchNum == 7.16):
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.11):
        hero.movement_speed = 295
    if(patchNum == 6.87):
        hero.movement_speed = 300
        hero.strength = 21
    if(patchNum == 6.85):
        hero.strength = 18
    return hero

def slardar(patchNum, hero):
    if(patchNum == 7.19):
        hero.armor -= 1
    if(patchNum == 6.87):
        hero.movement_speed = 295
    return hero

def spirit_breaker(patchNum, hero):
    if(patchNum == 7.20):
        hero.hp_regen -= 0.75
    if(patchNum == 7.15):
        hero.hp_regen = 1
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
        hero.hp_regen = 2
    if(patchNum == 7.05):
        hero.movement_speed = 290
    if(patchNum == 6.78):
        hero.base_attack_time = 1.7
    return hero

def sven(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 3.5
        hero.movement_speed -= 15
    if(patchNum == 7.19):
        hero.movement_speed = 290
    if(patchNum == 7.18):
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.05):
        hero.base_attack_time = 1.7
    if(patchNum == 6.86):
        hero.movement_speed = 295
    if(patchNum == 6.85):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.84):
        hero.intelligence = hero.intelligence - 2
    if(patchNum == 6.80):
        hero.damage_upper = hero.damage_upper - 6
        hero.damage_lower = hero.damage_lower - 6
        hero.damage_avg = hero.damage_avg - 6
    if(patchNum == 6.79):
        hero.armor = hero.armor - 3
    return hero

def tidehunter(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 3.8
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 6.82):
        hero.movement_speed = hero.movement_speed + 5
    return hero

def shredder(patchNum, hero):
    if(patchNum == 7.20):
        hero.intelligence -= 2
    if(patchNum == 7.19):
        hero.str_gain = 2.1
    if(patchNum == 7.12):
        hero.armor = hero.armor - 1 #counteract 7.13 attribute case
    if(patchNum == 7.06):
        hero.hp_regen = 0
    if(patchNum == 7.05):
        hero.str_gain = 1.8
        hero.hp_regen = 0.25
    if(patchNum == 6.87):
        hero.strength = 1.8
    if(patchNum == 6.79):
        hero.strength = 22
    return hero
 
def tiny(patchNum, hero):
    if(patchNum == 7.12):
        hero.armor = hero.armor - 1 #counteract 7.13 attribute case
    if(patchNum == 7.17):
        hero.str_gain = 3.3
    if(patchNum == 7.16):
        hero.movement_speed = 280
    if(patchNum == 7.11):
        hero.hp_regen = 2.5
    if(patchNum == 7.06):
        hero.strength = 26
        hero.hp_regen = 1.5
        hero.agi_gain = 0.9
        hero.agility = 9
        hero.armor = -1
    if(patchNum == 7.05):
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 7.04):
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 6.84):
        hero.strength = 24
        hero.intelligence = 14
    return hero
 
def treant_protector(patchNum, hero):
    if(patchNum == 7.11):
        hero.intelligence = 17
    if(patchNum == 7.05):
        hero.movement_speed = 290
        hero.str_gain = 3.3
    if(patchNum == 7.04):
        hero.movement_speed = 295
    if(patchNum == 6.87):
        hero.damage_upper = hero.damage_upper - 6
        hero.damage_lower = hero.damage_lower - 6
        hero.damage_avg = hero.damage_avg - 6
    return hero

def tusk(patchNum, hero):
    if(patchNum == 7.19):
        hero.str_gain = 3
    if(patchNum == 7.06):
        hero.str_gain = 2.6
    if(patchNum == 7):
        hero.turn_rate = 0.5
    if(patchNum == 6.85):
        hero.movement_speed = 305
    return hero

def underlord(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 5
        hero.intel_gain = 2.6
    if(patchNum == 7.01):
        hero.movement_speed = 305
    return hero

def undying(patchNum, hero):
    if(patchNum == 7.19):
        hero.movement_speed = 305
    if(patchNum == 7.05):
        hero.armor = hero.armor - 1
    if(patchNum == 6.87):
        hero.intel_gain = 2.5
    if(patchNum == 6.8):
        hero.intel_gain = 2
    return hero

def wraith_king(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 15
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
        hero.str_gain = 3.2
    if(patchNum == 6.84):
        hero.damage_upper = hero.damage_upper - 7
        hero.damage_lower = hero.damage_lower - 7
        hero.damage_avg = hero.damage_avg - 7
    if(patchNum == 6.8):
        hero.armor = 1
    if(patchNum == 6.78):
        hero.intelligence = 23
    return hero

#str heroes

def antimage(patchNum, hero):
    if(patchNum == 7.20):
        hero.agility -= 2
    if(patchNum == 7.16):
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
        hero.base_attack_time = 1.45
    if(patchNum == 7.12):
        hero.hp_regen = 1.5
    if(patchNum == 7.06):
        #hero.movement_speed = hero.movement_speed + 5
        hero.str_gain = 1.5
        hero.intelligence = 15
    if(patchNum == 6.81):
        hero.strength = 20
    return hero

def arc_warden(patchNum, hero):
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.12):
        hero.hp_regen = 1.5
    #if(patchNum == 7.06):
        #hero.movement_speed = 285
    if(patchNum == 7.05):
        hero.turn_rate = 0.4
    if(patchNum == 7.03):
        hero.str_gain = 2.3
    if(patchNum == 6.86):
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_avg = hero.damage_avg - 4
        hero.str_gain = 1.9
        hero.intel_gain = 2.1
    return hero 

def bloodseeker(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 5
    #if(patchNum == 7.06):
        #hero.movement_speed = 290
    if(patchNum == 7.05):
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.86):
        hero.str_gain = 2
    if(patchNum == 6.78):
        hero.movement_speed = 305
    return hero

def bounty_hunter(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 2.6
    if(patchNum == 7.19):
        hero.agi_gain = 3
        hero.strength = 18
        hero.str_gain = 2.1
    if(patchNum == 7.06):
        hero.hp_regen = 0.5
        #hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 7.05):
        hero.movement_speed = 315
    if(patchNum == 6.83):
        hero.intel_gain = 1.4
    return hero

def broodmother(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 2.5
    if(patchNum == 7.18):
        hero.agility = 18
    #if(patchNum == 7.06):
        #hero.movement_speed = 290
    return hero

def clinkz(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.attack_range = 640
    if(patchNum == 7.18):
        hero.strength = 16
    if(patchNum == 7.16):
        hero.armor = hero.armor - 1
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
        hero.intelligence = 16
        hero.intel_gain = 1.55
    if(patchNum == 7.12):
        hero.hp_regen = 1.5
    if(patchNum == 7.06):
        #hero.movement_speed = hero.movement_speed + 5
        hero.agi_gain = 3.3
    if(patchNum == 6.87):
        hero.attack_range = 630
    if(patchNum == 6.85):
        hero.agi_gain = 3
    if(patchNum == 6.82):
        hero.attack_range = 600
    return hero

def drow_ranger(patchNum, hero):
    if(patchNum == 7.19):
        hero.agility -= 4
    if(patchNum == 7.18):
        hero.agility = 26
        hero.agi_gain = 1.9
        hero.strength = hero.strength + 1
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 7.12):
        hero.hp_regen = 1.5
    #if(patchNum == 7.06):
        #hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 6.88):
        hero.movement_speed = hero.movement_speed + 10
    if(patchNum == 6.87):
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_avg = hero.damage_avg + 4
        hero.str_gain = 1.9
        hero.turn_rate = 0.6
    return hero

def ember_spirit(patchNum, hero):
    if(patchNum == 7.20):
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 7.19):
        hero.str_gain = 2.4
        hero.strength = 20
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.11):
        hero.armor = -2
    if(patchNum == 7.06):
        hero.hp_regen = .5
        #hero.movement_speed = 310
    if(patchNum == 7.04):
        hero.str_gain = 2
    return hero

def faceless_void(patchNum, hero):
    if (patchNum == 7.06):
        hero.hp_regen = 0.5
    if (patchNum == 7.04):
        hero.agi_gain = 2.65
    if(patchNum == 6.87):
        hero.armor = hero.armor + 1
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
    if(patchNum == 6.8):
        hero.agility = 21
        hero.turn_rate = 0.5
    return hero

def gyrocopter(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.agi_gain = 2.8
        hero.str_gain = 2.1
    if(patchNum == 7.18):
        hero.agility = 24
    if(patchNum == 7.05):
        hero.movement_speed = 315
    if(patchNum == 6.86):
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
    if(patchNum == 6.83):
        hero.intelligence = 23
    return hero

def juggernaut(patchNum, hero):
    if(patchNum == 7.20):
        hero.armor += 1
    if(patchNum == 7.20):
        hero.agility -= 10
    if(patchNum == 7.16):
        hero.armor = hero.armor - 1
    if(patchNum == 7.06):
        hero.hp_regen = 0.5
    if(patchNum == 7.04):
        hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 6.87):
        hero.damage_upper = hero.damage_upper + 2
        hero.damage_lower = hero.damage_lower + 2
        hero.damage_avg = hero.damage_avg + 2
    if(patchNum == 6.82):
        hero.agi_gain = 2.85
        hero.armor = hero.armor + 1
        hero.agility = 20
    if(patchNum == 6.8):
        hero.base_attack_time = 1.6
    return hero

def lone_druid(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.movement_speed = 320
        hero.armor += 2
        hero.agi_gain = 2.7
        hero.agility = 24
    if(patchNum == 7.06):
        hero.hp_regen == 0.25
        hero.turn_rate = 0.4
    if(patchNum == 7.02):
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
    return hero

def luna(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.agi_gain = 3.3
    if(patchNum == 7.06):
        hero.str_gain = 2.5
    if(patchNum == 7.01):
        hero.damage_upper = hero.damage_upper + 6
        hero.damage_lower = hero.damage_lower + 6
        hero.damage_avg = hero.damage_avg + 6
    if(patchNum == 7):
        hero.armor = hero.armor + 1
    if(patchNum == 6.87):
        hero.movement_speed = 330
    if(patchNum == 6.86):
        hero.agi_gain = 2.8
    if(patchNum == 6.85):
        hero.turn_rate = 0.4
    if(patchNum == 6.84):
        hero.str_gain = 1.9
    if(patchNum == 6.83):
        hero.armor = hero.armor - 1
    if(patchNum == 6.8):
        hero.agi = 22
    return hero

def medusa(patchNum, hero):
    if(patchNum == 7.20):
        hero.intel_gain = 2.1
    if(patchNum == 7.19):
        hero.agi_gain = 2.5
        hero.agility = 20
    if(patchNum == 7.06):
        hero.str_gain = 1.95
        hero.movement_speed = 290 
    if(patchNum == 6.87):
        hero.intel_gain = 1.85
    return hero

def meepo(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 1.6
        hero.agility = 23
        hero.str_gain = 1.6
    if(patchNum == 7.19):
        hero.agi_gain = 2.2
        hero.movement_speed = 310
    if(patchNum == 7.17):
        hero.armor = hero.armor - 2
    if(patchNum == 7.16):
        hero.armor = -1
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
    if(patchNum == 7.12):
        hero.hp_regen = 1.5
    if(patchNum == 7.06):
        hero.armor = hero.armor + 2
    if(patchNum == 6.87):
        hero.agi_gain = 1.9
    if(patchNum == 6.86):
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.8):
        hero.movement_speed = 305
    if(patchNum == 6.78):
        hero.armor = hero.armor + 1
        hero.turn_rate = .5
    return hero

def mirana(patchNum, hero):
    if(patchNum == 7.20):
        hero.intelligence = 17
        hero.intel_gain = 1.7
        hero.movement_speed += 5
    if(patchNum == 7.06):
        hero.agility = 20
        hero.agi_gain = 3.6
    if(patchNum == 7.05):
        hero.agi_gain = 3.3
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 6.85):
        hero.attack_range = 600
    if(patchNum == 6.84):
        hero.agi_gain = 2.75
    return hero

def monkey_king(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 5
    if(patchNum == 7.09):
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.06):
        hero.hp_regen = 1.5
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.05):
        hero.hp_regen = 0.75
    if(patchNum == 7.04):
        hero.str_gain = 2.2
    if(patchNum == 7.01):
        hero.armor = 0
    return hero

def morphling(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 2.3
    if(patchNum == 7.06):
        hero.intelligence = 17
    if(patchNum == 7.05):
        hero.base_attack_time = 1.6
    if(patchNum == 6.87):
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_avg = hero.damage_avg + 4
        hero.agi_gain = 3.4
    if(patchNum == 6.84):
        hero.agi_gain = 3
    return hero

def naga_siren(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 5
    if(patchNum == 7.06):
        hero.agi_gain = 2.75
        hero.hp_regen = 1.5
    if(patchNum == 7.05):
        hero.hp_regen = 0.5
    if(patchNum == 6.87):
        hero.str_gain = 2.3
    if(patchNum == 6.85):
        hero.intelligence = 18
        hero.intel_gain = 1.95
    return hero

def nyx_assassin(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 5
        hero.str_gain = 2.3
    if(patchNum == 7.06):
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 6.87):
        hero.movement_speed = 300
    return hero

def pangolier(patchNum, hero):
    if(patchNum == 7.20):
        hero.damage_avg = hero.damage_avg - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_upper = hero.damage_upper - 4
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
    if(patchNum == 7.12):
        hero.hp_regen = 1.5
    return hero

def phantom_assassin(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 3.7
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
    if(patchNum == 7.06):
        hero.movement_speed = 310
    if(patchNum == 6.86):
        hero.intelligence = 13
        hero.intel_gain = 1
    return hero 

def phantom_lancer(patchNum, hero):
    if(patchNum == 7.19):
        hero.intelligence += 2
    if(patchNum == 7.18):
        hero.agi_gain = 2.8
        hero.intelligence = hero.intelligence + 2
    if(patchNum == 7.17):
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.06):
        hero.hp_regen = 1.5
    if(patchNum == 7.05):
        hero.agi_gain = 2.6
        hero.hp_regen = 0.5
    if(patchNum == 6.84):
        hero.agi_gain = 3
    if(patchNum == 6.81):
        hero.agility = 23
        hero.agi_gain = 4.2
        hero.strength = 18
    return hero

def razor(patchNum, hero):
    if(patchNum == 7.06):
        hero.movement_speed = hero.movement_speed + 5
        hero.turn_rate = 0.4
    if(patchNum == 7.05):
        hero.agi_gain = 2
    if(patchNum == 7.04):
        hero.intelligence = 19
    if(patchNum == 6.8):
        hero.str_gain = 1.7
    return hero

def riki(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 10
        hero.damage_avg -= 4
        hero.damage_upper -= 4
        hero.damage_lower -= 4
    if(patchNum == 7.17):
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 7.16):
        hero.armor = 0
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_lower = hero.damage_lower - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 7.06):
        hero.agility = 34
        hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 7.05):
        hero.movement_speed = 290
        hero.str_gain = 1.6
    if(patchNum == 6.85):
        hero.str_gain = 2
        hero.agi_gain = 2.9
        hero.armor = 1
    if(patchNum == 6.81):
        hero.movement_speed = 300
        hero.damage_upper = 14
        hero.damage_lower = 18
        hero.damage_avg = 16
        hero.hp_regen = 1.5
    if(patchNum == 6.79):
        hero.hp_regen = 0.75
    return hero

def shadow_fiend(patchNum, hero):
    if(patchNum == 7.20):
        hero.strength -= 3
        hero.intel_gain = 2.0
        hero.movement_speed += 5
        hero.armor -= 1
    if(patchNum == 7.19):
        hero.armor -= 1
    if(patchNum == 7.06):
        hero.hp_regen = 0.25
    if(patchNum == 6.88):
        hero.movement_speed = 305
    if(patchNum == 6.85):
        hero.armor = hero.armor + 1
    return hero

def slark(patchNum, hero):
    if(patchNum == 7.20):
        hero.armor -= 1
    if(patchNum == 7.19):
        hero.turn_rate = 0.6
    if(patchNum == 7.13):
        hero.hp_regen = 2.75
    if(patchNum == 7.11):
        hero.hp_regen = 1.5
        hero.turn_rate = 0.5
    if(patchNum == 7.05):
        hero.intel_gain = 1.9
    if(patchNum == 7.01):
        hero.movement_speed = 305
    if(patchNum == 7):
        hero.strength = 21
        hero.str_gain = 1.8
    return hero

def sniper(patchNum, hero):
    if(patchNum == 7.20):
        hero.strength -= 2
    if(patchNum == 7.15):
        hero.night_vision = 1100
    if(patchNum == 7.14):
        hero.strength = 16
    if(patchNum == 7.06):
        hero.str_gain = 2
    if(patchNum == 7.05):
        hero.agi_gain = 2.5
    if(patchNum == 6.87):
        hero.turn_rate = 0.6
        hero.night_vision = 1000
    if(patchNum == 6.83):
        hero.agi_gain = 2.9
    return hero

def spectre(patchNum, hero):
    if(patchNum == 7.20):
        hero.strength = 2
        hero.str_gain = 2.3
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 7.05):
        hero.strength = 19
    if(patchNum == 6.86):
        hero.agi_gain = 2.2
    return hero

def templar_assassin(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 2.6
        hero.movement_speed += 5
    if(patchNum == 7.15):
        hero.hp_regen = 1.75
    if(patchNum == 7.11):
        hero.movement_speed = 300
    if(patchNum == 7.05):
        hero.agi_gain = 2.7
    return hero

def terror_blade(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 1.7
        hero.strength = 16
    if(patchNum == 7.17):
        hero.agi_gain = 3.7
    if(patchNum == 7.16):
        hero.agi_gain = 3.2
    if(patchNum == 7.13):
        hero.hp_regen = 3
    if(patchNum == 7.09):
        hero.hp_regen = 3.25
    if(patchNum == 7.06):
        hero.intel_gain = 1.75
        hero.hp_regen = 1.75
    if(patchNum == 6.86):
        hero.armor = 4
    if(patchNum == 6.8):
        hero.str_gain = 1.9
    return hero
 
def troll_warlord(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed -= 5
    if(patchNum == 7.19):
        hero.damage_avg = (38+56)/2
        hero.damage_lower = 38
        hero.damage_upper = 56
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
    if(patchNum == 7.06):
        hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 7.05):
        hero.agi_gain = 2.75
    if(patchNum == 6.87):
        hero.strength = 17
    return hero
  
def ursa(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
        hero.armor += 2
        hero.movement_speed = 305
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.13):
        hero.armor = 3
    if(patchNum == 7.12):
        hero.str_gain = 3
    if(patchNum == 7.06):
        hero.movement_speed = hero.movement_speed + 5
        hero.hp_regen = .5
    if(patchNum == 7.05):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 6.87):
        hero.hp_regen = .25
    if(patchNum == 6.84):
        hero.str_gain = 2.9
    return hero
 
def vengefulspirit(patchNum, hero):
    if(patchNum == 7.18):
        hero.movement_speed = 295
    if(patchNum == 7.15):
        hero.hp_regen = 1.5
    if(patchNum == 7.06):
        hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 6.84):
        hero.agi_gain = 2.8
        hero.movement_speed = 295
    return hero
 
def venomancer(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 1.9
    if(patchNum == 7.19):
        hero.agility -= 4
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
        hero.movement_speed = hero.movement_speed + 5
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.05):
        hero.str_gain = 2.15
        hero.agi_gain = 2.6
        hero.str_gain = 1.85
    if(patchNum == 6.87):
        hero.intelligence = 15
        hero.intel_gain = 1.75
    if(patchNum == 6.79):
        hero.damage_upper = hero.damage_upper + 5
        hero.damage_lower = hero.damage_lower + 5
        hero.damage_avg = hero.damage_avg + 5
        hero.hp_regen = 0.75
    if(patchNum == 6.78):
        hero.movement_speed = 290
    return hero

def viper(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 3.3
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
        hero.movement_speed = hero.movement_speed + 5
        hero.armor = hero.armor + 1
    if(patchNum == 6.87):
        hero.str_gain = 1.9
    if(patchNum == 6.84):
        hero.agi_gain = 2.5
    return hero

def weaver(patchNum, hero):
    if(patchNum == 7.18):
        hero.intelligence = 15
        hero.movement_speed = 280
    if(patchNum == 7.17):
        hero.agi_gain = 2.8
    if(patchNum == 7.13):
        hero.hp_regen = 1.5
    if(patchNum == 7.02):
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_avg = hero.damage_avg + 3
        hero.movement_speed = 290
    if(patchNum == 7.01):
        hero.damage_upper = hero.damage_upper + 2
        hero.damage_lower = hero.damage_lower + 2
        hero.damage_avg = hero.damage_avg + 2
    if(patchNum == 6.88):
        hero.agi_gain = 2.5
    if(patchNum == 6.87):
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 6.85):
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 6.78):
        hero.base_attack_time = 1.7
    return hero

#agi heroes

def ancient_apparition(patchNum, hero):
    if(patchNum == 7.20):
        hero.intel_gain = 3
    if(patchNum == 7.14):
        hero.damage_lower = 19
        hero.damage_upper = 29
        hero.damage_avg = (19 + 29) / 2.0
    if(patchNum == 7.05):
        hero.str_gain = 1.4
        hero.attack_range = 600
    return hero

def bane(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 2.4
        hero.agi_gain = 2.4
        hero.intel_gain = 2.8
    if(patchNum == 7.16):
        hero.damage_lower = hero.damage_lower + 2
        hero.damage_upper = hero.damage_upper + 2
        hero.damage_avg = hero.damage_avg + 2
    if(patchNum == 7.14):
        hero.intelligence = hero.intelligence - 2 #counteract -2 int to all int heroes
    if(patchNum == 7.05):
        hero.strength = 22
        hero.intelligence = 22
        hero.agility = 22
        hero.str_gain = 2.1
        hero.intel_gain = 2.1
        hero.agi_gain = 2.1
    if(patchNum == 7.02):
        hero.damage_lower = hero.damage_lower - 4 
        hero.damage_upper = hero.damage_upper - 4
        hero.damage_avg = hero.damage_avg - 4
    if(patchNum == 6.85):
        hero.movement_speed = 315
    return hero

def batrider(patchNum, hero):
    if(patchNum == 7.13):
        hero.strength = 25
    if(patchNum == 7.06):
        hero.hp_regen = 1.75
    if(patchNum == 6.85):
        hero.hp_regen = 0.25
    if(patchNum == 6.78):
        hero.damage_lower = 48
        hero.damage_upper = 52
        hero.damage_avg = 50
    return hero

def chen(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.06):
        hero.attack_range = 600
    if(patchNum == 6.85):
        hero.strength = 20
    return hero

def crystal_maiden(patchNum, hero):
    if(patchNum == 7.19):
        hero.damage_avg -= 2
        hero.damage_upper -= 2
        hero.damage_lower -= 2
    if(patchNum == 7.15):
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.13):
        hero.armor = -1
    if(patchNum == 7.11):
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 7.05):
        hero.movement_speed = 280
    if(patchNum == 6.79):
        hero.intelligence = hero.intelligence + 3
    if(patchNum == 6.78):
        hero.intelligence = 21
    return hero

def dark_seer(patchNum, hero):
    if(patchNum == 7.20):
        hero.armor += 2
        hero.agi_gain = 1.2
    if(patchNum == 7.12):
        hero.str_gain = 2.6
        hero.strength = 22
    if(patchNum == 7.05):
        hero.intelligence = 25
    if(patchNum == 7.01):
        hero.movement_speed = 300
    if(patchNum == 6.85):
        hero.intelligence = 27
    if(patchNum == 6.84):
        hero.intelligence = 29
    if(patchNum == 6.82):
        hero.armor = 4
    return hero
 
def dark_willow(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    #no changes
    return hero

def dazzle(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.intel_gain = 3.4
    if(patchNum == 7.17):
        hero.damage_lower = hero.damage_lower - 6
        hero.damage_upper = hero.damage_upper - 6
        hero.damage_avg = hero.damage_avg - 6
    if(patchNum == 7.15):
        hero.str_gain = 2.15
    if(patchNum == 7.09):
        hero.movement_speed = 305
    if(patchNum == 6.82):
        hero.attack_range = 500
    return hero

def death_prophet(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
        hero.damage_avg -= 3
        hero.damage_upper -= 3
        hero.damage_lower -= 3
    if(patchNum == 7.19):
        hero.movement_speed = 305
    if(patchNum == 7.17):
        hero.armor += 1
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.17):
        hero.armor = hero.armor + 1
    if(patchNum == 7.15):
        hero.movement_speed = 310
    if(patchNum == 7.13):
        hero.hp_regen = 2
    if(patchNum == 7.06):
        hero.hp_regen = .5
    if(patchNum == 7.05):
        hero.str_gain = 2.3
    if(patchNum == 7.04):
        hero.str_gain = 1.9
    if(patchNum == 6.87):
        hero.strength = 18
    if(patchNum == 6.86):
        hero.strength = 19
    if(patchNum == 6.85):
        hero.intelligence = 20
    if(patchNum == 6.82):
        hero.str_gain = 2.2
    return hero
 
def disruptor(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
        hero.armor -= 1
    #no changes
    return hero

def enchantress(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.armor -= 2
    if(patchNum == 7.18):
        hero.strength = 19
        hero.str_gain = 1.3
        hero.intelligence = 19
        hero.movement_speed = 340
    if(patchNum == 7.17):
        hero.attack_range = 550
    if(patchNum == 7.15):
        hero.strength = 18
    if(patchNum == 7.07):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 7.05):
        hero.intelligence = 17
    if(patchNum == 7.04):
        hero.intel_gain = 2.8
    if(patchNum == 7.02):
        hero.movement_speed = 335
    if(patchNum == 7):
        hero.intelligence = hero.intelligence - 3
    if(patchNum == 6.82):
        hero.movement_speed = 315
    if(patchNum == 6.81):
        hero.movement_speed = 310
    if(patchNum == 6.79):
        hero.armor = hero.armor + 1
    if(patchNum == 6.78):
        hero.night_vision = 1800
    return hero

def enigma(patchNum, hero):
    if(patchNum == 7.19):
        hero.movement_speed = 300
    if(patchNum == 7.06):
        hero.strength = 17
    return hero

def grimstroke(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    #nothing here bois
    return hero

def invoker(patchNum, hero):
    if(patchNum == 7.20):
        hero.damage_avg -= 3
        hero.damage_lower -= 3
        hero.damage_upper -= 3
    if(patchNum == 7.04):
        hero.strength = 17
    if(patchNum == 7):
        hero.str_gain = 1.7
    if(patchNum == 6.86):
        hero.intelligence = 22
    if(patchNum == 6.85):
        hero.strength = 19
    if(patchNum == 6.84):
        hero.intel_gain = 3.2
    if(patchNum == 6.83):
        hero.intel_gain = 2.5
    return hero

def jakiro(patchNum, hero):
    if(patchNum == 7.14):
        hero.intelligence = 28
        hero.damage_lower = hero.damage_lower - 2 
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg  - 2
    if(patchNum == 6.85):
        hero.damage_lower = 18
        hero.damage_upper = 26
        hero.damage_avg = (18+26)/2.0
    if(patchNum == 6.83):
        hero.strength = 24
    return hero

def keeper_of_the_light(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.14):
        hero.damage_lower = 18
        hero.damage_upper = 25
        hero.damage_avg = (18+25)/2.0
    if(patchNum == 7.03):
        hero.damage_lower = 43
        hero.damage_upper = 57
        hero.damage_avg = (43+57)/2.0
    if(patchNum == 6.87):
        hero.intelligence = 22
    if(patchNum == 6.86):
        hero.movement_speed = 315
    return hero

def leshrac(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 1.7
        hero.movement_speed += 5
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.15):
        hero.intelligence = hero.intelligence + 2
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.11):
        hero.movement_speed = 325
    if(patchNum == 6.87):
        hero.movement_speed = 320
    if(patchNum == 6.84):
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_avg = hero.damage_avg + 4
    if(patchNum == 6.83):
        hero.movement_speed = 315
    return hero
 
def lich(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed = 310
    if(patchNum == 7.19):
        hero.intel_gain = 3.3
        hero.intelligence = 16
    
    return hero

def lina(patchNum, hero):
    if(patchNum == 7.20):
        hero.intelligence -= 2
        hero.movement_speed += 5
        hero.damage_lower -= 3
        hero.damage_upper -= 3
        hero.damage_avg -= 3
    if(patchNum == 7.19):
        hero.armor -= 2
    if(patchNum == 7.07):
        hero.intelligence = hero.intelligence - 3
    if(patchNum == 6.87):
        hero.base_attack_time = 1.7
    if(patchNum == 6.80):
        hero.attack_range = 650
    if(patchNum == 6.78):
        hero.attack_range = 635
    return hero

def lion(patchNum, hero):
    if(patchNum == 7.14):
        hero.intelligence = 20
        hero.damage_lower = 27
        hero.damage_upper = 33
        hero.damage_avg = (27+33)/2
    if(patchNum == 7.05):
        hero.str_gain = 1.7
    if(patchNum == 6.86):
        hero.intelligence = 22
    if(patchNum == 6.82):
        hero.damage_lower = 20
        hero.damage_upper = 26
        hero.damage_avg = 23
    return hero

def furion(patchNum, hero):
    if(patchNum == 7.20):
        hero.agi_gain = 2.8
    if(patchNum == 7.19):
        hero.agi_gain = 2.4
        hero.armor -= 1
    if(patchNum == 7.18):
        hero.damage_avg += 3
        hero.damage_upper += 3
        hero.damage_lower += 3
    if(patchNum == 7.17):
        hero.agi_gain = 1.9
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.18):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.17):
        hero.agi_gain = 1.9
    if(patchNum == 7.05):
        hero.movement_speed = 295
    if(patchNum == 7.04):
        hero.damage_lower = hero.damage_lower - 6
        hero.damage_upper = hero.damage_upper - 6
        hero.damage_avg = hero.damage_avg - 6
    if(patchNum == 6.85):
        hero.intelligence = hero.intelligence - 4
    return hero
 
def necrophos(patchNum, hero):
    if(patchNum == 7.19):
        hero.attack_range = 550
    if(patchNum == 7.18):
        hero.agility = 15
        hero.agi_gain = 1.2
        hero.movement_speed = 285
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.18):
        hero.agility = 15
        hero.agi_gain = 1.2
        hero.movement_speed = 285
    if(patchNum == 7.15):
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.01):
        hero.agi_gain = 1.7
        hero.movement_speed = 290
    if(patchNum == 7.85):
        hero.armor = 0
    if(patchNum == 6.78):
        hero.armor = -1
    return hero
 
def ogre_magi(patchNum, hero):
    if(patchNum == 7.06):
        hero.hp_regen = 3.25
    if(patchNum == 7.01):
        hero.movement_speed = 290
        hero.intel_gain = 2.4
    if(patchNum == 7):
        hero.movement_speed = 295
    if(patchNum == 6.85):
        hero.hp_regen = 2.5
    if(patchNum == 6.84):
        hero.armor = 5
    if(patchNum == 6.81):
        hero.hp_regen = 0.25
    if(patchNum == 6.8):
        hero.armor = 4
    return hero

def oracle(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.17):
        hero.intel_gain = 3.2
    if(patchNum == 7.09):
        hero.turn_rate = 0.5
        hero.intel_gain = 2.9
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 6.87):
        hero.damage_lower = hero.damage_lower + 6
        hero.damage_upper = hero.damage_upper + 6
        hero.damage_avg = hero.damage_avg + 6
    return hero

def outworld_devourer(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
        hero.intel_gain = 2.7
        hero.armor -= 1
        hero.intelligence = 24
    if(patchNum == 7.12):
        hero.strength = hero.strength + 2 #counteract -2 str to all int heroes
    if(patchNum == 6.87):
        hero.damage_lower = hero.damage_lower + 6
        hero.damage_upper = hero.damage_upper + 6
        hero.damage_avg = hero.damage_avg + 6
        hero.armor = hero.armor + 1.5
    if(patchNum == 6.84):
        hero.str_gain = 1.85
    if(patchNum == 6.78):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    return hero

def puck(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
        hero.armor -= 1
        hero.intel_gain = 2.4
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 7.05):
        hero.armor = hero.armor + 1
    if(patchNum == 7.03):
        hero.damage_lower = hero.damage_lower - 3
        hero.damage_upper = hero.damage_upper - 3
        hero.damage_avg = hero.damage_avg - 3
    if(patchNum == 7.02):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 7.01):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 6.78):
        hero.night_vision = 1200
    return hero

def pugna(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.18):
        hero.damage_lower = hero.damage_lower + 2
        hero.damage_upper = hero.damage_upper + 2
        hero.damage_avg = hero.damage_avg + 2
    if(patchNum == 7.13):
        hero.armor = -1
    if(patchNum == 7.12):
        hero.str_gain = 1.5
    if(patchNum == 7.05):
        hero.attack_range = 600
        hero.movement_speed = 330
    if(patchNum == 6.87):
        hero.intel_gain = 4
    if(patchNum == 6.84):
        hero.movement_speed = 320
    return hero

def queen_of_pain(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
        hero.agility = 18
        hero.agi_gain = 2
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7.05):
        hero.damage_lower = hero.damage_lower + 4
        hero.damage_upper = hero.damage_upper + 4
        hero.damage_avg = hero.damage_avg + 4
    if(patchNum == 6.88):
        hero.base_attack_time = 1.6
    if(patchNum == 6.83):
        hero.movement_speed = 300
    if(patchNum == 6.81):
        hero.base_attack_time = 1.7
    return hero

def rubick(patchNum, hero):
    if(patchNum == 7.19):
        hero.agility = 14
        hero.agi_gain = 1.6
        hero.damage_lower -= 3
        hero.damage_upper -= 3
        hero.damage_avg -= 3
        hero.intelligence = 2.4
    if(patchNum == 7.14):
        hero.intelligence = 27
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.02):
        hero.attack_range = 600
    if(patchNum == 6.86):
        hero.turn_rate = 0.5
    return hero

def shadow_demon(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.13):
        hero.str_gain = 2.2
    if(patchNum == 7.05):
        hero.strength = 17
    return hero

def shadow_shaman(patchNum, hero):
    if(patchNum == 7.18):
        hero.armor = hero.armor - 1
    if(patchNum == 7.16):
        hero.intelligence = 19
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 7.05):
        hero.damage_lower = hero.damage_lower - 6
        hero.damage_upper = hero.damage_upper - 6
        hero.damage_avg = hero.damage_avg - 6
    if(patchNum == 7.02):
        hero.armor = hero.armor - 1
        hero.attack_range = 500
        hero.damage_lower = hero.damage_lower - 18
        hero.damage_upper = hero.damage_upper - 18
        hero.damage_avg = hero.damage_avg - 18
    return hero

def silencer(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 6.87):
        hero.agility = 16
    if(patchNum == 6.83):
        hero.movement_speed = 300
    if(patchNum == 6.8):
        hero.agi_gain = 2.1
    return hero

def skywrath_mage(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.04):
        hero.movement_speed = 325
    if(patchNum == 6.82):
        hero.agility = 18
    if(patchNum == 6.8):
        hero.movement_speed = 315
    if(patchNum == 6.78):
        hero.intel_gain = 3.2
    return hero

def storm_spirit(patchNum, hero):
    if(patchNum == 7.20):
        hero.damage_avg -= 2
        hero.damage_upper -= 2
        hero.damage_lower -= 2
        hero.intel_gain = 3
    if(patchNum == 7.06):
        hero.agi_gain = 1.8
    if(patchNum == 6.86):
        hero.intelligence = 23
        hero.intel_gain = 2.6
    if(patchNum == 6.83):
        hero.movement_speed = 290
    if(patchNum == 6.82):
        hero.turn_rate = 0.6
    if(patchNum == 6.79):
        hero.movement_speed = 295
    return hero

def techies(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.19):
        hero.movement_speed = 270
        hero.intelligence -= 2
    return hero

def tinker(patchNum, hero):
    if(patchNum == 7.12):
        hero.strength = hero.strength + 2 #counteract -2 str to all int heroes
    if(patchNum == 7.07):
        hero.movement_speed = 305
    if(patchNum == 6.86):
        hero.intelligence = 27
    return hero

def visage(patchNum, hero):
    if(patchNum == 7.20):
        hero.str_gain = 3.2
        hero.strength = 24
    if(patchNum == 7.12):
        hero.str_gain = hero.str_gain - 0.3
    if(patchNum == 7):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
    if(patchNum == 6.79):
        hero.movement_speed = hero.movement_speed + 5
    if(patchNum == 6.78):
        hero.armor = hero.armor + 1
        hero.magic_res = 25
    return hero

def warlock(patchNum, hero):
    if(patchNum == 7.20):
        hero.intelligence -= 3
        hero.movement_speed += 5
        hero.strength -= 2
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    if(patchNum == 6.85):
        hero.strength = hero.strength - 4
    return hero

def windranger(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.17):
        hero.intelligence = hero.intelligence + 2
    if(patchNum == 7.06):
        hero.turn_rate = 0.6
    return hero

def winter_wyvern(patchNum, hero):
    if(patchNum == 7.16):
        hero.intelligence = 24
    if(patchNum == 7.11):
        hero.intelligence = hero.intelligence - 1
    if(patchNum == 7.06):
        hero.damage_lower = hero.damage_lower + 3
        hero.damage_upper = hero.damage_upper + 3
        hero.damage_avg = hero.damage_avg + 3
        hero.turn_rate = 0.4
    return hero

def witch_doctor(patchNum, hero):
    if(patchNum == 7.20):
        hero.movement_speed += 5
    if(patchNum == 7.06):
        hero.turn_rate = 0.4
    return hero

def zeus(patchNum, hero):
    if(patchNum == 7.18):
        hero.str_gain = 2.3
    if(patchNum == 7.15):
        hero.damage_lower = hero.damage_lower - 5
        hero.damage_upper = hero.damage_upper -5 
        hero.damage_avg = hero.damage_avg - 5
        hero.str_gain = 2.6
    if(patchNum == 7.14):
        hero.intelligence = 22
        hero.damage_lower = hero.damage_lower - 2
        hero.damage_upper = hero.damage_upper - 2
        hero.damage_avg = hero.damage_avg - 2
    if(patchNum == 7.11):
        hero.attack_range = 350
        hero.damage_lower = hero.damage_lower - 5
        hero.damage_upper = hero.damage_upper - 5
        hero.damage_avg = hero.damage_avg - 5
    if(patchNum == 7.05):
        hero.movement_speed = 295
    if(patchNum == 7.04):
        hero.intelligence = 20
    return hero


#end hero specific functions


'''
The list starts on the newest patch and contains all patches going to patch 6.78. When adding a new patch, add another patch into this function
'''

Listpatch = []
def init_ListPatch():
    patch = Patch(7.21)
    Listpatch.append(patch)
    patch = Patch(7.20)
    Listpatch.append(patch)
    patch = Patch(7.19)
    Listpatch.append(patch)
    patch = Patch(7.18)
    Listpatch.append(patch)
    patch = Patch(7.17)
    Listpatch.append(patch)
    patch = Patch(7.16)
    Listpatch.append(patch)
    patch = Patch(7.15)
    Listpatch.append(patch)
    patch = Patch(7.14)
    Listpatch.append(patch)
    patch = Patch(7.13)
    Listpatch.append(patch)
    patch = Patch(7.12)
    Listpatch.append(patch)
    patch = Patch(7.11)
    Listpatch.append(patch)
    patch = Patch(7.1)
    Listpatch.append(patch)
    patch = Patch(7.09)
    Listpatch.append(patch)
    patch = Patch(7.08)
    Listpatch.append(patch)
    patch = Patch(7.07)
    Listpatch.append(patch)
    patch = Patch(7.06)
    Listpatch.append(patch)
    patch = Patch(7.05)
    Listpatch.append(patch)
    patch = Patch(7.04)
    Listpatch.append(patch)
    patch = Patch(7.03)
    Listpatch.append(patch)
    patch = Patch(7.02)
    Listpatch.append(patch)
    patch = Patch(7.01)
    Listpatch.append(patch)
    patch = Patch(7)
    Listpatch.append(patch)
    patch = Patch(6.88)
    Listpatch.append(patch)
    patch = Patch(6.87)
    Listpatch.append(patch)
    patch = Patch(6.86)
    Listpatch.append(patch)
    patch = Patch(6.85)
    Listpatch.append(patch)
    patch = Patch(6.84)
    Listpatch.append(patch)
    patch = Patch(6.83)
    Listpatch.append(patch)
    patch = Patch(6.82)
    Listpatch.append(patch)
    patch = Patch(6.81)
    Listpatch.append(patch)
    patch = Patch(6.8)
    Listpatch.append(patch)
    patch = Patch(6.79)
    Listpatch.append(patch)
    patch = Patch(6.78)
    Listpatch.append(patch)

init_ListPatch() #calls the function to create of list of empty patches



#initialize patches to be a copy of the first patch in the patch list

def initialize_patchs(patchList):
    for x in range(len(patchList)-1):
        patchList[x+1].heroes = copy.deepcopy(patchList[x].heroes)


'''
This is where we make changes to several heroes at once. This also takes the official hero name found in the wiki and calls the appriate hero function to calculate changes.
'''

def calculate_stats(patch_num, heroes):
    for i in range(len(heroes)):
        #attribute cases
        #An example here is that in patch 7.04, all agi hereos movement speed was reduced by 5.
        if(patch_num == 7.05 and heroes[i].attribute == 'agi'):
            heroes[i].movement_speed = heroes[i].movement_speed + 5
        if(patch_num == 7.05):
            heroes[i].hp_regen = heroes[i].hp_regen + 0.25
            heroes[i].str_gain = heroes[i].str_gain - 0.3
        if(patch_num == 7.12 and heroes[i].attribute == 'str'):
            heroes[i].movement_speed = heroes[i].movement_speed + 5
            heroes[i].armor = heroes[i].armor + 1
        if(patch_num == 7.12 and heroes[i].attribute == 'int'):
            heroes[i].strength = heroes[i].strength - 2
        if(patch_num == 7.14 and heroes[i].attribute == 'agi'):
            heroes[i].strength = heroes[i].strength - 1
        if(patch_num == 7.14 and heroes[i].attribute == 'int'):
            heroes[i].intelligence = heroes[i].intelligence + 2
        if(patch_num == 7.06 and heroes[i].attribute == 'agi'):
            heroes[i].movement_speed = heroes[i].movement_speed + 5


        #hero specific cases
        if(heroes[i].hero_id == 'npc_dota_hero_antimage'):
            heroes[i] = antimage(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_arc_warden'):
            heroes[i] = arc_warden(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_bloodseeker'):
            heroes[i] = bloodseeker(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_bounty_hunter'):
            heroes[i] = bounty_hunter(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_broodmother'):
            heroes[i] = broodmother(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_clinkz'):
            heroes[i] = clinkz(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_drow_ranger'):
            heroes[i] = drow_ranger(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_ember_spirit'):
            heroes[i] = ember_spirit(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_faceless_void'):
            heroes[i] = faceless_void(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_gyrocopter'):
            heroes[i] = gyrocopter(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_juggernaut'):
            heroes[i] = juggernaut(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_lone_druid'):
            heroes[i] = lone_druid(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_luna'):
            heroes[i] = luna(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_medusa'):
            heroes[i] = medusa(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_meepo'):
            heroes[i] = meepo(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_mirana'):
            heroes[i] = mirana(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_monkey_king'):
            heroes[i] = monkey_king(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_morphling'):
            heroes[i] = morphling(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_naga_siren'):
            heroes[i] = naga_siren(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_nevermore'):
            heroes[i] = shadow_fiend(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_nyx_assassin'):
            heroes[i] = pangolier(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_phantom_assassin'):
            heroes[i] = phantom_assassin(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_phantom_lancer'):
            heroes[i] = phantom_lancer(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_razor'):
            heroes[i] = razor(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_riki'):
            heroes[i] = riki(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_slark'):
            heroes[i] = slark(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_sniper'):
            heroes[i] = sniper(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_spectre'):
            heroes[i] = spectre(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_templar_assassin'):
            heroes[i] = templar_assassin(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_terrorblade'):
            heroes[i] = terror_blade(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_troll_warlord'):
            heroes[i] = troll_warlord(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_ursa'):
            heroes[i] = ursa(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_vengefulspirit'):
            heroes[i] = vengefulspirit(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_venomancer'):
            heroes[i] = venomancer(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_viper'):
            heroes[i] = viper(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_weaver'):
            heroes[i] = weaver(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_willow'):
            heroes[i] = dark_willow(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_ancient_apparition'):
            heroes[i] = ancient_apparition(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_bane'):
            heroes[i] = bane(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_batrider'):
            heroes[i] = batrider(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_chen'):
            heroes[i] = chen(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_crystal_maiden'):
            heroes[i] = crystal_maiden(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_dark_seer'):
            heroes[i] = dark_seer(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_dazzle'):
            heroes[i] = dazzle(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_death_prophet'):
            heroes[i] = death_prophet(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_disruptor'):
            heroes[i] = disruptor(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_enchantress'):
            heroes[i] = enchantress(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_enigma'):
            heroes[i] = enigma(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_furion'):
            heroes[i] = furion(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_invoker'):
            heroes[i] = invoker(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_jakiro'):
            heroes[i] = jakiro(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_keeper_of_the_light'):
            heroes[i] = keeper_of_the_light(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_leshrac'):
            heroes[i] = leshrac(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_lich'):
            heroes[i] = lich(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_lina'):
            heroes[i] = lina(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_lion'):
            heroes[i] = lion(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_necrolyte'):
            heroes[i] = necrophos(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_obsidian_destroyer'):
            heroes[i] = outworld_devourer(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_ogre_magi'):
            heroes[i] = ogre_magi(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_oracle'):
            heroes[i] = oracle(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_puck'):
            heroes[i] = puck(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_pugna'):
            heroes[i] = pugna(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_queenofpain'):
            heroes[i] = queen_of_pain(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_rubick'):
            heroes[i] = rubick(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_shadow_demon'):
            heroes[i] = shadow_demon(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_shadow_shaman'):
            heroes[i] = shadow_shaman(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_silencer'):
            heroes[i] = silencer(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_skywrath_mage'):
            heroes[i] = skywrath_mage(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_storm_spirit'):
            heroes[i] = storm_spirit(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_techies'):
            heroes[i] = techies(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_tinker'):
            heroes[i] = tinker(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_visage'):
            heroes[i] = visage(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_warlock'):
            heroes[i] = warlock(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_windrunner'):
            heroes[i] = windranger(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_winter_wyvern'):
            heroes[i] = winter_wyvern(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_witch_doctor'):
            heroes[i] = witch_doctor(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_zuus'):
            heroes[i] = zeus(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_abaddon'):
            heroes[i] = abaddon(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_abyssal_underlord'):
            heroes[i] = underlord(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_alchemist'):
            heroes[i] = alchemist(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_axe'):
            heroes[i] = axe(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_beastmaster'):
            heroes[i] = beastmaster(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_brewmaster'):
            heroes[i] = brewmaster(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_bristleback'):
            heroes[i] = bristleback(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_centaur'):
            heroes[i] = centaur(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_chaos_knight'):
            heroes[i] = chaos_knight(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_doom_bringer'):
            heroes[i] = doom(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_dragon_knight'):
            heroes[i] = dragon_knight(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_earth_spirit'):
            heroes[i] = earth_spirit(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_earthshaker'):
            heroes[i] = earth_shaker(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_elder_titan'):
            heroes[i] = elder_titan(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_huskar'):
            heroes[i] = huskar(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_kunkka'):
            heroes[i] = kunkka(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_legion_commander'):
            heroes[i] = legion_commander(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_life_stealer'):
            heroes[i] = lifestealer(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_lycan'):
            heroes[i] = lycan(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_magnataur'):
            heroes[i] = magnus(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_night_stalker'):
            heroes[i] = nightstalker(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_omniknight'):
            heroes[i] = omniknight(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_phoenix'):
            heroes[i] = phoenix(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_pudge'):
            heroes[i] = pudge(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_rattletrap'):
            heroes[i] = clockwerk(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_sand_king'):
            heroes[i] = sand_king(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_skeleton_king'):
            heroes[i] = wraith_king(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_shredder'):
            heroes[i] = shredder(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_slardar'):
            heroes[i] = slardar(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_spirit_breaker'):
            heroes[i] = spirit_breaker(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_sven'):
            heroes[i] = sven(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_tidehunter'):
            heroes[i] = tidehunter(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_tiny'):
            heroes[i] = tiny(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_treant'):
            heroes[i] = treant_protector(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_tusk'):
            heroes[i] = tusk(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_undying'):
            heroes[i] = undying(patch_num, heroes[i])
        elif(heroes[i].hero_id == 'npc_dota_hero_wisp'):
            heroes[i] = wisp(patch_num, heroes[i])



            
'''
This is for doing calculations with the stats. Calculating hp mp and armor at lvl 25 varies per patch as well as the engine rounds down the value when
doing the calculations.
'''
def calc_attribute(patch_num, heroes):
    for i in range(len(heroes)):
        if(patch_num >= 7.13):
            if(heroes[i].attribute=='str'):
                heroes[i].level_1_hp = round(200 + float(heroes[i].strength)*22.5,2)
                heroes[i].level_15_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*14))*22.5,2)
                heroes[i].level_25_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*24))*22.5,2)
            else:
                heroes[i].level_1_hp = round(200 + float(heroes[i].strength)*18,2)
                heroes[i].level_15_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*14))*18,2)
                heroes[i].level_25_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*24))*18,2)
            if(heroes[i].attribute=='int'):
                heroes[i].level_1_mp = round(75 + float(heroes[i].intelligence)*15,2)
                heroes[i].level_15_mp = round(75 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*14)*15,2)
                heroes[i].level_25_mp = round(75 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*24)*15,2)
            else:
                heroes[i].level_1_mp = round(75 + float(heroes[i].intelligence)*12,2)
                heroes[i].level_15_mp = round(75 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*14)*12,2)
                heroes[i].level_25_mp = round(75 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*24)*12,2)
            if(heroes[i].attribute=='agi'):
                heroes[i].level_1_armor = round(float(heroes[i].armor) + float(heroes[i].agility)*0.2,2)
                heroes[i].level_15_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*14))*0.2,2)
                heroes[i].level_25_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*24))*0.2,2)
            else:
                heroes[i].level_1_armor = round(float(heroes[i].armor) + float(heroes[i].agility)*0.16,2)
                heroes[i].level_15_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*14))*0.16,2)
                heroes[i].level_25_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*24))*0.16,2)
        elif(patch_num >= 7.06):
            heroes[i].level_1_hp = round(200 + float(heroes[i].strength)*20,2)
            heroes[i].level_15_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*14))*20,2)
            heroes[i].level_25_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*24))*20,2)
            heroes[i].level_1_mp = round(75 + float(heroes[i].intelligence)*12,2)
            heroes[i].level_15_mp = round(75 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*14)*12,2)
            heroes[i].level_25_mp = round(75 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*24)*12,2)
            heroes[i].level_1_armor = round(float(heroes[i].armor) + float(heroes[i].agility)*0.17,2)
            heroes[i].level_15_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*14))*0.17,2)
            heroes[i].level_25_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*24))*0.17,2)
        else:
            heroes[i].level_1_hp = round(200 + float(heroes[i].strength)*20,2)
            heroes[i].level_15_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*14))*20,2)
            heroes[i].level_25_hp = round(200 + (float(heroes[i].strength)+math.floor(float(heroes[i].str_gain)*24))*20,2)
            heroes[i].level_1_mp = round(50 + float(heroes[i].intelligence)*11,2)
            heroes[i].level_15_mp = round(50 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*14)*11,2)
            heroes[i].level_25_mp = round(50 + float(heroes[i].intelligence)+math.floor(float(heroes[i].intel_gain)*24)*11,2)
            heroes[i].level_1_armor = round(float(heroes[i].armor) + float(heroes[i].agility)*0.17,2)
            heroes[i].level_15_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*14))*0.17,2)
            heroes[i].level_25_armor = round(float(heroes[i].armor) + (float(heroes[i].agility)+math.floor(float(heroes[i].agi_gain)*24))*0.17,2)

#load in hero stats

'''
There must be a current copy of the hero stats from the newest patch for which to build the rest of the matches onto. This will load in the data.
'''

with open('hero_stats721.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if(line_count == 0):
            line_count += 1
        else:
            #adding from first csv file
            Listpatch[0].heroes.append(Hero(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 
                row[8], row[12], row[13], row[14], 
                row[15], row[17], row[18], row[19], row[20], 
                row[21], row[22], row[23], row[24], row[25], row[26], row[27]))


'''
With the current patch loaded in, initialize_patches will copy the current patch to all other patches.
'''
initialize_patchs(Listpatch)
print("finished init")


'''
This is to call all of the previous functions on a given patch and apply all the changes made to that patch. Then we take all the changes made to
the patch and waterfall it down to all the other patches that come before it.
'''

for x in range(len(Listpatch)):
    calculate_stats(Listpatch[x].patch_num, Listpatch[x].heroes)
    calc_attribute(Listpatch[x].patch_num, Listpatch[x].heroes)
    initialize_patchs(Listpatch[x:])

#populate buff/nerf

'''
Since a hero will be both buffed and nerfed in a single patch (buffed in patch 7.19, nerfed in 7.19b) we must figure out if the hero 
is buffed or nerfed for the entirety of that patch. We then import this data and assign the proper nerf/buff status to the proper hero in 
the proper patch. This must be done seperatly because we need to explicilty have nerf/buff for each hero and for each patch while the stats 
can be derived from the patch before it. This must be updated to include new patches
'''

# with open('buff7_18.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if(line_count == 0):
#             line_count += 1 #column names
#         else:
#             Listpatch[1].heroes[line_count-1].nerf_buff = copy.deepcopy(row[1])
#             line_count += 1

with open('hero_buffs.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = -1
    for row in csv_reader:
        if(line_count == -1):
            line_count += 1
        else:
            for i in range(len(row)-1):
                Listpatch[i].heroes[line_count].nerf_buff = row[i+1]
            line_count += 1
            
'''
This is for printing out hero attributes for debugging. This will print certain attributes for certain heroes for all the patches.
'''

for x in range(len(Listpatch)):
    for i in range(len(Listpatch[x].heroes)):
        z = Listpatch[x]
        if(z.heroes[i].hero_id == 'npc_dota_hero_bristleback'):
            print(str(z.patch_num) + ": " + z.heroes[i].hero_id + " ms: " + str(z.heroes[i].movement_speed) + " armor: " + 
            str(z.heroes[i].armor) + " damage_avg: " + str(z.heroes[i].damage_avg) + "nerf/buff: " + z.heroes[i].nerf_buff)

'''
Saving each patch to its own csv file.
'''
for x in range(len(Listpatch)):
    name = round(Listpatch[x].patch_num,2)
    with open("%f.csv" %name, "w") as f:
        writer = csv.writer(f)
        for i in range(len(Listpatch[x].heroes)):
            writer.writerow(Listpatch[x].heroes[i])
