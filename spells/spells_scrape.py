#!/usr/bin/env python
# -*- coding: utf8 -*-
import numpy as np
import pandas as pd
pd.options.display.max_columns = 200

# For getting data from the web
import requests, json, re

from bs4 import BeautifulSoup

# For working with temporal data
from datetime import datetime

import copy
import time

Patchlistnames = ['7.19','7.18','7.17','7.16','7.15','7.14','7.13','7.12','7.11','7.10','7.1','7.09','7.08','7.07',
'7.06','7.05','7.04','7.03','7.02','7.01','7.00','6.88','6.87','6.86','6.85','6.84','6.83','6.82','6.81',
'6.80','6.8','6.79','6.78']

tempParses = 'parsed.txt'
endParse = 'endparsed.txt'

#writing
fileo = open(tempParses,'a')
filee = open(endParse, 'w')

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
    time.sleep(3)
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
    
    time.sleep(35)
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
            time.sleep(35)
            json_response = requests.get(query_string).json()
            subquery_revision_list = json_response['query']['pages'][pageid]['revisions']
            revision_list += subquery_revision_listß

    df = pd.DataFrame(revision_list)
    df['page'] = page_title
    df['userid'] = df['userid'].fillna(0).apply(lambda x:str(int(x)))
    
    return df

#heroID = [ 'Abaddon', 'Alchemist', 'Axe', 'Beastmaster', 'Brewmaster', 'Bristleback', 'Centaur_Warrunner', 'Chaos_Knight', 'Clockwerk', 'Doom', 'Dragon_Knight', 'Earth_Spirit', 'Elder_Titan', 'Huskar', 'Io', 'Kunkka', 'Legion_Commander', 'Lifestealer', 'Lycan', 'Magnus', 'Night_Stalker', 'Omniknight', 'Phoenix', 'Pudge', 'Sand_King', 'Slardar', 'Spirit_Breaker', 'Sven', 'Tidehunter', 'Timbersaw', 'Tiny', 'Treant_Protector', 'Tusk', 'Underlord', 'Undying', 'Wraith_King', 'Anti-Mage', 'Arc_Warden', 'Bloodseeker', 'Bounty_Hunter', 'Broodmother', 'Clinkz,' 'Drow_Ranger', 'Ember_Spirit', 'Faceless_Void', 'Gyrocopeter', 'Juggernaut', 'Lone_Druid', 'Luna', 'Medusa', 'Meepo', 'Mirana', 'Monkey_King', 'Morphling', 'Naga_Siren', 'Nyx_Assassin', 'Pangolier', 'Phantom_Assassin', 'Phantom_Lancer', 'Razor', 'Riki', 'Shadow_Fiend', 'Slark', 'Sniper', 'Spectre', 'Templar_Assassin', 'Terrorblade', 'Troll_Warlord', 'Ursa', 'Vengeful_Spirit', 'Venomancer', 'Viper', 'Weaver', 'Ancient_Apparition', 'Bane', 'Batrider', 'Chen', 'Crystal_Maiden', 'Dark_Seer', 'Dark_Willow', 'Dazzle', 'Death_Prophet', 'Disruptor', 'Enchantress', 'Enigma', 'Grimstroke', 'Invoker', 'Jakiro', 'Keeper_of_the_Light', 'Leshrac', 'Lich', 'Lina', 'Lion', 'Nature%27s_Prophet', 'Necrophos', 'Ogre_Magi', 'Oracle', 'Outworld_Devourer', 'Puck', 'Pugna', 'Queen_of_Pain', 'Rubick', 'Shadow_Demon', 'Shadow_Shaman', 'Silencer', 'Skywrath_Mage', 'Storm_Spirit', 'Techies', 'Tinker', 'Visage', 'Warlock', 'Windranger', 'Winter_Wyvern', 'Witch_Doctor', 'Zeus']
heroID = ['Lycan', 'Magnus', 'Night_Stalker', 'Omniknight', 'Phoenix', 'Pudge', 'Sand_King', 'Slardar', 'Spirit_Breaker', 'Sven', 'Tidehunter', 'Timbersaw', 'Tiny', 'Treant_Protector', 'Tusk', 'Underlord', 'Undying', 'Wraith_King', 'Anti-Mage', 'Arc_Warden', 'Bloodseeker', 'Bounty_Hunter', 'Broodmother', 'Clinkz,' 'Drow_Ranger', 'Ember_Spirit', 'Faceless_Void', 'Gyrocopeter', 'Juggernaut', 'Lone_Druid', 'Luna', 'Medusa', 'Meepo', 'Mirana', 'Monkey_King', 'Morphling', 'Naga_Siren', 'Nyx_Assassin', 'Pangolier', 'Phantom_Assassin', 'Phantom_Lancer', 'Razor', 'Riki', 'Shadow_Fiend', 'Slark', 'Sniper', 'Spectre', 'Templar_Assassin', 'Terrorblade', 'Troll_Warlord', 'Ursa', 'Vengeful_Spirit', 'Venomancer', 'Viper', 'Weaver', 'Ancient_Apparition', 'Bane', 'Batrider', 'Chen', 'Crystal_Maiden', 'Dark_Seer', 'Dark_Willow', 'Dazzle', 'Death_Prophet', 'Disruptor', 'Enchantress', 'Enigma', 'Grimstroke', 'Invoker', 'Jakiro', 'Keeper_of_the_Light', 'Leshrac', 'Lich', 'Lina', 'Lion', 'Nature%27s_Prophet', 'Necrophos', 'Ogre_Magi', 'Oracle', 'Outworld_Devourer', 'Puck', 'Pugna', 'Queen_of_Pain', 'Rubick', 'Shadow_Demon', 'Shadow_Shaman', 'Silencer', 'Skywrath_Mage', 'Storm_Spirit', 'Techies', 'Tinker', 'Visage', 'Warlock', 'Windranger', 'Winter_Wyvern', 'Witch_Doctor', 'Zeus']



tempFile = ""
endFile = ""
loop = True
#call get_page_revisions for each hero
#import pdb; pdb.set_trace()
for q in range(0, len(heroID)):
    time.sleep(35)
    hero_name = heroID[q]
    revision_list = get_page_revisions(hero_name)
    for index, row in revision_list.iterrows():
        if(row['comment'] in Patchlistnames):
            while(loop == True):
                try:
                    time.sleep(35)
                    api = 'https://liquipedia.net/dota2/api.php'
                    params = {}
                    params['action'] = 'parse'
                    params['format'] = 'json'
                    params['oldid'] = row['parentid']
                    params['prop'] = 'text'

                    json_response = requests.get(api,params).json()
                    html = json_response['parse']['text']['*']

                    soup = BeautifulSoup(html, 'lxml')
                    for x in range(0,5):
                        try:
                            print('patch num: ' + row['comment'])
                            stuff=soup.find_all('div',{'class':'spellcard panel-primary'})[x].text.split("\n")
                            spellId = soup.find_all(class_="spellcard-wrapper")
                            print(stuff)
                            tempFile += 'Patch' + row['comment'] + 'Hero' + hero_name + 'Spell_Name' + spellId[x].get('id') + ' ' + stuff[0] + '\n'
                        except:
                            print(" ")
                            pass
                    tempFile += '\n'
                    endFile += tempFile
                    fileo.write(tempFile.encode('ascii', 'ignore').decode('ascii'))
                    tempFile = ''
                    loop = False
                except:
                    s = input("Press enter to continue")
                    print("catch error on spellcard info\n")
                    pass

filee.write(endFile.encode('ascii', 'ignore').decode('ascii'))

#-------------------------------------------------------------------------------------------
print("--------------------------------------------------------")
