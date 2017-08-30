# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 15:54:24 2017

@author: Boulot
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 21:24:12 2017

@author: Boulot
"""

#with open(r"C:\Users\Boulot\Desktop\population-communes-belges.tsv") as f:
#    communes = f.readlines()
        

import requests
import time

def get_wikipedia_page2(value):

    if type(value) is str:
        value = value.title()
        for lang in ["fr", "nl", "en"]:
            
            url = "https://{}.wikipedia.org/w/api.php?".format(lang)
    
            payload = {"format":"json",
                       "action":"query",
                       "generator":"search",
                       "gsrnamespace":0,
                       "gsrsearch":value,
                       "gsrlimit":20,
                       "prop":"categories|extracts|info|revisions|pageprops",
                       "inprop":"url",
                       "ppprop":"wikibase_item",
                       "rvprop":"content",
                       "exintro":"",
                       "explaintext":"",
                       "exsentences":1,
                       "exlimit":"max",
                       "cllimit":"max"}
            
            r = requests.get(url, params=payload).json()
            try:
                for pageid, page in r["query"]["pages"].items():
                    try:
                        if page['title'].startswith(value) or page['title'].startswith("Ville"):
                            if "belgi" in page['extract'].lower():
                                for cat in page['categories']:                                        
                                    if ("commune" in cat['title'].lower() 
                                        or "ville" in cat['title'].lower()
                                        or "localité" in cat['title'].lower() 
                                        or "plaats" in cat['title'].lower() 
                                        or "municipalit" in cat['title'].lower()
                                        or "city" in cat['title'].lower()):
                                        
                                        info = (page['title'], 
                                                page['fullurl'],
                                                page['length'],
                                                page['categories'],
                                                page['extract'],
                                                page['pageprops']['wikibase_item'])
                                                #page['revisions'])
                                        return info
                                        break

                    except KeyError:
                        continue             
    
            except (KeyError, UnboundLocalError):
                 return None

def get_geonames(value):
    url = "http://api.geonames.org/searchJSON?" 

    
    payload = {"q":value,
            "maxRows":1,
            "country":"BE",
            "style":"full",
            "lang=":"FR",
            "username":"ettorerizza"}
    if len(value) >= 1:
        try:
            r = requests.get(url, params=payload)
        
            return r.json()["geonames"][0]["toponymName"]
        except IndexError:
            pass

def get_wikipedia_page(value):
    try:

        if type(value) is str:
            value = value
            for lang in ["fr", "nl", "en"]:
                
                url = "https://{}.wikipedia.org/w/api.php?".format(lang)
        
                payload = {"format":"json",
                           "action":"query",
                           "titles":value,
                           "exlimit":5,
                           "prop":"categories|extracts|info|revisions|pageprops",
                           "inprop":"url",
                           "ppprop":"wikibase_item",
                           "exintro":"",
                           "explaintext":"",
                           "redirects":"",
                           "rvprop":"content"}
                
                r = requests.get(url, params=payload).json()
                for pageid, page in r["query"]["pages"].items():
                    homonym = False
                    for cat in page['categories']:
                        #print(cat)
                        if "Homonymie" in cat['title'] or "Doorverwijspagina" in cat['title'] or "Disambiguation" in cat['title']:
                            homonym = True
                        elif ("commune" in cat['title'].lower() 
                            or "ville" in cat['title'].lower()
                            or "localité" in cat['title'].lower() 
                            or "plaats" in cat['title'].lower() 
                            or "municipalit" in cat['title'].lower()
                            or "city" in cat['title'].lower()):
                            info = (page['title'], 
                                    page['fullurl'],
                                    page['length'],
                                    page['categories'],
                                    page['extract'],
                                    page['pageprops']['wikibase_item'])
                                    #page['revisions'])
                            return info
                            break
                        else:
                            continue


                        if homonym == True:
                            #print("homonyme")
                            continue
                        
                return info   
    except:
        return None 

#print(get_wikipedia_page("braine-le-comte"))
#print(get_wikipedia_page2("braine-le-comte"))
               
def get_wikipedia_element(ville):
    try:
        resp = get_wikipedia_page(ville)
        if resp == None:
            resp = get_wikipedia_page2(ville)
        (title, url, length, categories, extract, wikidata) = resp
        return url
    except TypeError:
        return None
    
start_time = time.time()
print(get_wikipedia_element("braine-le-comte")) 
print("--- %s seconds ---" % (time.time() - start_time))

#print(get_geonames("munsterbilsen"))
#liste = []
#for c in communes:
#    liste.append(get_wikipedia_element(c.strip()))
#print(liste)
#
#with open(r"C:\Users\Boulot\Desktop\liste.tsv", "w") as f:
#    for i in liste:
#        f.write(i + "\n")
    