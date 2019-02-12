#!/usr/bin/env python
# -*- coding: utf8 -*-
import numpy as np
import pandas as pd
pd.options.display.max_columns = 200

# For plotting data
#import matplotlib.pyplot as plt
#import seaborn as sb
#%matplotlib inline

# For getting data from the web
import requests, json, re

from bs4 import BeautifulSoup

# For working with temporal data
from datetime import datetime

import copy


#general questions: Help including manacost and cooldown for heroes with passives and the like. Right now im attempting some super shoddy stuff that COULD work with absorbant effort.
#Thoughts on modifier (used to think i could assign it to stun/slow/silence but is proving difficult)
#When a spell only has damage, how to make sure it only considers it as damage instead of considering DPS as damage because it reads it as part of the substring. (possible solution is to fix the if-then statements in the parser)
#Do i need to worry about including future patches?
#What should I do if a spell would be accepted by parser but shouldn't. (eg lifestealer and his lifesteal ability)

class Spell:
    '''def __init__(self, name, targeting, affects, damageType, damage, damagePerSecond, damagePercent, damagePercentPerSecond, healing, healingPerSecond,
                 healingPercent, healingPercentPerSecond, hpregen, critDamage, critChance, lifeSteal, mana, cooldown, cast_time, modifier, duration, aoe):
        self.name = name
        self.targeting = targeting
        self.affects = affects
        self.damageType = damageType
        self.damage = damage
        self.damagePerSecond = damagePerSecond
        self.damagePercent = damagePercent
        self.damagePercentPerSecond = damagePercentPerSecond
        self.healing = healing
        self.healingPerSecond = healingPerSecond
        self.healingPercent = healingPercent
        self.healingPercentPerSecond = healingPercentPerSecond
        self.hpRegen = hpregen
        self.critDamage = critDamage
        self.critChance = critChance
        self.lifeSteal = lifeSteal
        self.mana = mana
        self.cooldown = cooldown
        self.cast_time = cast_time
        self.modifier = modifier
        self.duration = duration
        self.aoe = aoe #size of aoe. 0 if no aoe

    '''
    patch = 0
    hero_name = ''
    name = ''
    targeting = '' #allied hero, aoe, enemyaoe, enemy single, toggle aoe (wk),
    affects = ''
    damageType = ''
    damage = 0
    damagePerSecond = 0
    damagePercent = 0
    damagePercentPerSecond = 0
    healing = 0
    healingPerSecond = 0
    healingPercent = 0
    healingPercentPerSecond = 0
    hpRegen = 0
    critDamage = 0
    critChance = 0
    lifeSteal = 0 #worried about lifestealer
    mana = 0
    cooldown = 0
    cast_time = 0
    modifier = '' #initilially thought to consider the modifier as the silence/stun/slow to reduce columns but that seems incredibly hard. Will figure out semantics
    duration = 0
    aoe = 0
    

    def __iter__(self):
        return iter([self.patch, self.hero_name, self.name, self.targeting, self.affects, self.damageType, self.damage, self.damagePerSecond, self.damagePercent,
                 self.damagePercentPerSecond, self.healing, self.healingPerSecond,
                 self.healingPercent, self.healingPercentPerSecond, self.critDamage, self.critChance, self.lifeSteal, self.mana, self.cooldown,
                 self.cast_time, self.modifier, self.duration, self.aoe])
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__



Patchlistnames = ['7.19','7.18','7.17','7.16','7.15','7.14','7.13','7.12','7.11','7.10','7.1','7.09','7.08','7.07',
'7.06','7.05','7.04','7.03','7.02','7.01','7.00','7.0','7','6.88','6.87','6.86','6.85','6.84','6.83','6.82','6.81',
'6.80','6.8','6.79','6.78']

savedParses = 'parsed.txt'

#writing
#file = open(savedParses,'w')
#reading
file = open(savedParses,'r')

def get_rev_content(revid,lang='en',redirects=1,parsed_text=1):
    """Takes a revision id and returns a (large) string of the HTML content 
    of the revision.
    
    revid - a numeric revision id as a string
    lang - a string (typically two letter ISO 639-1 code) for the language 
        edition, defaults to "en"
    redirects - 1 or 0 for whether to follow page redirects, defaults to 1
    parse - 1 or 0 for whether to return the raw HTML or paragraph text
    
    Returns:
    str - a (large) string of the content of the revision
    """
    
    bad_titles = ['Special:','Wikipedia:','Help:','Template:','Category:','International Standard','Portal:','s:','File:','Digital object identifier','(page does not exist)']
    
    # Get the response from the API for a query
    # After passing a page title, the API returns the HTML markup of the current article version within a JSON payload
    #req = requests.get('https://{2}.wikipedia.org/w/api.php?action=parse&format=json&oldid={0}&redirects={1}&prop=text&disableeditsection=1&disabletoc=1'.format(revid,redirects,lang))
    req = requests.get('https://liquipedia.net/dota2/api.php?action=parse&format=json&oldid={0}&redirects={1}&prop=text&disableeditsection=1&disabletoc=1'.format(revid,redirects,lang))
    
    # Read the response into JSON to parse and extract the HTML
    json_string = json.loads(req.text)
    
    if 'parse' in json_string.keys():
        page_html = json_string['parse']['text']['*']

        # Parse the HTML into Beautiful Soup
        soup = BeautifulSoup(page_html,'lxml')
        
        # Remove sections at end
        bad_sections = ['See_also','Notes','References','Bibliography','External_links']
        sections = soup.find_all('h2')
        for section in sections:
            if section.span['id'] in bad_sections:
                
                # Clean out the divs
                div_siblings = section.find_next_siblings('div')
                for sibling in div_siblings:
                    sibling.clear()
                    
                # Clean out the ULs
                ul_siblings = section.find_next_siblings('ul')
                for sibling in ul_siblings:
                    sibling.clear()
        
        # Get all the paragraphs
        paras = soup.find_all('p')
        
        text_list = []
        
        for para in paras:
            if parsed_text:
                _s = para.text
                # Remove the citations
                _s = re.sub(r'\[[0-9]+\]','',_s)
                text_list.append(_s)
            else:
                text_list.append(str(para))
        
        return '\n'.join(text_list)

print("printing_rev_content: \n")
#something = get_rev_content(634621)
#print(something)
#-------------------------------------------------------------------------------------
print("--------------------------------------------------------")
print("printing spell card info")
api = 'https://liquipedia.net/dota2/api.php'
params = {}
params['action'] = 'parse'
params['format'] = 'json'
params['oldid'] = 634621
#oldid found through tools>find_permanent_link
params['prop'] = 'text'

#remove comment to make calls

json_response = requests.get(api,params).json()
html = json_response['parse']['text']['*']

soup = BeautifulSoup(html, 'lxml')




#https://stackoverflow.com/questions/25370255/python-get-a-html-element-node-tag-from-exact-position
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#https://stackoverflow.com/questions/11936967/text-file-parsing-with-python
#https://stackoverflow.com/questions/430079/how-to-split-strings-into-text-and-number

spells = []
spellId = soup.find_all(class_="spellcard-wrapper")
href = soup.find_all('a', href=True) #list of url calls in page
z = 0
for a in soup.find_all('a', href=True):
    print(str(z) + 'Found URL: ', a['href'])
    z += 1

#get hero names
hero_name = soup.find_all('div',{'class':'infobox-header wiki-backgroundcolor-light'})
hero_name = hero_name[0].text
hero_name = hero_name[6:]

'''
matches = []
#attempting to track mana and cooldowns by using url for each picture
for x in range(len(href)):
    #print(href[x]['href'])
    temp_spell_name = (str('/dota2/File:' + hero_name + '_' + spell1.name.lower() + '.png')).lower()
    #print("url: " + href[x]['href'])
    #print("mat: " + temp_spell_name)
    if((str(href[x]['href'])).lower() == temp_spell_name):
        print('found match')
        print('/dota2/File:'+ hero_name + '_' + spell1.name.lower() + '.png')
        print(x)
        matches.append(x)


#attempt to track cooldowns and mana
print('len of matches: ' + str(len(matches)))
for x in range(len(matches)-1):
    for i in range(matches[x],matches[x+1]):
        if(str(href[i]['href']).lower() == '/dota2/Cooldown'.lower()):
            print('found cooldown') #implement stuff to include cooldown
        if(str(href[i]['href']).lower() == '/dota2/Mana_Cost'.lower()):
            print('found manacost') #implement stuff to include manacost
'''


#loops for the number of spells
for i in range(4):
    stuff = soup.find_all('div',{'class':'spellcard panel-primary'})[i].text.split("\n") #get data from spellcards
    names = soup.find_all('div',{'class':'spellcard-wrapper'}) #get name of spell
    cooldownmana = soup.find_all('div',{'style':'display:inline-block; vertical-align:top; padding:5px 15px 0 0;'}) #get cooldown and mana positions
    
    
    print(spellId[i].get('id'))
    items = re.split("(a-zA-Z]+)([0-9]+)", stuff[0])
    #print(stuff[0])
    words = re.split('(\d+)',items[0])
    locs = len(words)
    print('size of each spell: ' + str(locs))
    
    spell1 = Spell() #lvl 1
    spell2 = Spell() #lvl 2
    spell3 = Spell() #lvl 3
    spell4 = Spell() #lvl 4
    
    spell1.name = spellId[i].get('id') #assign name
    spell2.name = spell1.name
    spell3.name = spell1.name
    spell4.name = spell1.name

    for x in range(locs):
        #print(str(x) + ": " + str(words[x]))
        if(words[x].find('Damage') != -1 and words[x+1].find('/') != -1): #make sure to debug
            spell1.damage = copy.deepcopy(words[x+1])
            spell2.damage = copy.deepcopy(words[x+3])
            spell3.damage = copy.deepcopy(words[x+5])
            spell4.damage = copy.deepcopy(words[x+7])
        elif(words[x].find('Damage') != -1): #make sure to only include damage and not dps or anything else
            spell1.damage = copy.deepcopy(words[x+1])
            spell2.damage = spell1.damage
            spell3.damage = spell1.damage
            spell4.damage = spell1.damage        
        if(words[x].find('Damage Per Second') != -1):
            spell1.damagePerSecond = copy.deepcopy(words[x+1])
            spell2.damagePerSecond = copy.deepcopy(words[x+3])
            spell3.damagePerSecond = copy.deepcopy(words[x+5])
            spell4.damagePerSecond = copy.deepcopy(words[x+7])
        if(words[x].find('Max HP bonus DPS') != -1 and words[x+1].find('/') != -1): #make sure to debug
            spell1.damagePercentPerSecond = copy.deepcopy(words[x+1])
            spell2.damagePercentPerSecond = copy.deepcopy(words[x+3])
            spell3.damagePercentPerSecond = copy.deepcopy(words[x+5])
            spell4.damagePercentPerSecond = copy.deepcopy(words[x+7])
        if(words[x].find('HP Regen') != -1 and words[x+1].find('/') != -1): #make sure to debug
            spell1.hpRegen = copy.deepcopy(words[x+1])
            spell2.hpRegen = spell1.hpRegen
            spell3.hpRegen = spell1.hpRegen
            spell4.hpRegen = spell1.hpRegen
        elif(words[x].find('HP Regen') != -1):
            spell1.hpRegen = copy.deepcopy(words[x+1])
            spell2.hpRegen = copy.deepcopy(words[x+3])
            spell3.hpRegen = copy.deepcopy(words[x+5])
            spell4.hpRegen = copy.deepcopy(words[x+7])
        if(words[x].find('Duration') != -1 and words[x+1].find('/') != -1):
            spell1.duration = copy.deepcopy(words[x+1])
            spell2.duration = copy.deepcopy(words[x+3])
            spell3.duration = copy.deepcopy(words[x+5])
            spell4.duration = copy.deepcopy(words[x+7])
        elif(words[x].find('Duration') != -1):
            spell1.duration = copy.deepcopy(words[x+1])
            spell2.duration = copy.deepcopy(words[x+1])
            spell3.duration = copy.deepcopy(words[x+1])
            spell4.duration = copy.deepcopy(words[x+1])
        if(words[x].find('Cast Point') != -1):
            spell1.cast_time = copy.deepcopy(words[x+1])
            spell2.cast_time = copy.deepcopy(words[x+1])
            spell4.cast_time = copy.deepcopy(words[x+1])
            spell3.cast_time = copy.deepcopy(words[x+1])
        if(words[x].find('Radius') != -1 and words[x+1].find('/') != -1):
            spell1.aoe = copy.deepcopy(words[x+1])
            spell2.aoe = copy.deepcopy(words[x+3])
            spell3.aoe = copy.deepcopy(words[x+5])
            spell4.aoe = copy.deepcopy(words[x+7])
        elif(words[x].find('Radius') != -1):
            spell1.aoe = copy.deepcopy(words[x+1])
            spell2.aoe = copy.deepcopy(words[x+1])
            spell3.aoe = copy.deepcopy(words[x+1])
            spell4.aoe = copy.deepcopy(words[x+1])
        if(words[x].find('Max HP Heal Per Second') != -1):
            spell1.healingPercentPerSecond = copy.deepcopy(words[x+1])
            spell2.healingPercentPerSecond = copy.deepcopy(words[x+3])
            spell3.healingPercentPerSecond = copy.deepcopy(words[x+5])
            spell4.healingPercentPerSecond = copy.deepcopy(words[x+7])
        elif(words[x].find('Heal Per Second') != -1):
            spell1.healingPerSecond = copy.deepcopy(words[x+1])
            spell2.healingPerSecond = copy.deepcopy(words[x+3])
            spell3.healingPerSecond = copy.deepcopy(words[x+5])
            spell4.healingPerSecond = copy.deepcopy(words[x+7])
        if(words[x].find('Critical Damage') != -1 and words[x+1].find('/') != -1):
            spell1.critDamage = copy.deepcopy(words[x+1])
            spell2.critDamage = copy.deepcopy(words[x+3])
            spell3.critDamage = copy.deepcopy(words[x+5])
            spell4.critDamage = copy.deepcopy(words[x+7])
        elif(words[x].find('Critical Damage') != -1):
            spell1.critDamage = copy.deepcopy(words[x+1])
            spell2.critDamage = copy.deepcopy(words[x+1])
            spell3.critDamage = copy.deepcopy(words[x+1])
            spell4.critDamage = copy.deepcopy(words[x+1])
        if(words[x].find('Critical Chance') != -1 and words[x+2].find('/') != -1): #x+2 if no talent
            spell1.critChance = copy.deepcopy(words[x+1])
            spell2.critChance = copy.deepcopy(words[x+3])
            spell3.critChance = copy.deepcopy(words[x+5])
            spell4.critChance = copy.deepcopy(words[x+7])
        elif(words[x].find('Critical Chance') != -1):
            spell1.critChance = copy.deepcopy(words[x+1])
            spell2.critChance = spell1.critChance
            spell3.critChance = spell1.critChance
            spell4.critChance = spell1.critChance
        if(words[x].find('Lifesteal') != -1):
            spell1.lifeSteal = copy.deepcopy(words[x+1])
            spell2.lifeSteal = copy.deepcopy(words[x+3])
            spell3.lifeSteal = copy.deepcopy(words[x+5])
            spell4.lifeSteal = copy.deepcopy(words[x+7])
        if(spell1 == Spell()):
            continue

    spells.append(spell1)
    spells.append(spell2)
    spells.append(spell3)
    spells.append(spell4)

for x in range(16):
    print("name: " + str(spells[x].name))
    print("dps: " + str(spells[x].damagePerSecond))
    print("duration: " + str(spells[x].duration))
    print("radius: " + str(spells[x].aoe))
    print("cast time: " + str(spells[x].cast_time))
    print("max hp heal per sec: " + str(spells[x].healingPercentPerSecond))
    print("hp heal per sec: " + str(spells[x].healingPerSecond))
    print("crit chance: " + str(spells[x].critChance))
    print("crit damage: " + str(spells[x].critDamage))
    print("lifeSteal: " + str(spells[x].lifeSteal))

#-------------------------------------------------------------------------------------------
print("--------------------------------------------------------")
print("printing page revisions") 
def get_page_revisions(page_title):
    """Takes Wikipedia page title and returns a DataFrame of revisions
    
    page_title - a string with the title of the page on Wikipedia
    lang - a string (typically two letter ISO 639-1 code) for the language edition,
        defaults to "en"
        
    Returns:
    df - a pandas DataFrame where each row is a revision and columns correspond
         to meta-data such as parentid, revid,sha1, size, timestamp, and user name
    """
    
    revision_list = list()
    
    query_string = "http://liquipedia.net/dota2/api.php?action=query&titles={0}&prop=revisions&rvprop=ids|userid|comment| \
                    timestamp|user|size|sha1&rvlimit=500&rvdir=older&format=json".format(page_title) 
    
    json_response = requests.get(query_string).json()
    pageid = list(json_response['query']['pages'].keys())[0]
    subquery_revision_list = json_response['query']['pages'][pageid]['revisions']
    revision_list += subquery_revision_list
    
    while True:

        if 'continue' not in json_response:
            break

        else:
            query_continue = json_response['continue']['rvcontinue']
            query_string = "http://liquipedia.net/dota2/api.php?action=query&titles={0}&prop=revisions&rvprop=ids| \
            timestamp|user|size|sha1&rvlimit=500&rvcontinue={2}&rvdir=older&format=json&formatversion=2".format(page_title,lang,query_continue)
            json_response = requests.get(query_string).json()
            subquery_revision_list = json_response['query']['pages'][pageid]['revisions']
            revision_list += subquery_revision_list
            #time.sleep(1)

    df = pd.DataFrame(revision_list)
    df['page'] = page_title
    df['userid'] = df['userid'].fillna(0).apply(lambda x:str(int(x)))
    
    return df

