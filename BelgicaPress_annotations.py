
# coding: utf-8

# In[73]:

import pandas as pd
import re
import time
import pandasql as pdsql #le sql est plus facile pour moi que pandas pour l'instant
pysql = lambda q: pdsql.sqldf(q, globals()) #petit réglage pour faciliter l'emploi de pandasql
import numpy as np
from unidecode import unidecode
import requests
import simplejson as json
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia
import difflib

pd.set_option('display.max_rows', None) #pour visualiser toutes les lignes des dataframes, pas si gros dans ce cas-ci



# In[6]:

annot = pd.read_csv(r'C:\Users\Boulot\Desktop\annotations_towork.csv', encoding="utf-8-sig", engine="c")
annot.head()
print(annot.columns.tolist())

annot.drop("equality_match_extract_geonames", axis=1)


# In[7]:

geo = pd.read_csv(r"C:\Users\Boulot\Desktop\geonames_be_cleaned.csv", encoding="utf8")
lieux_be = geo.noms
lieux_be = set([name.strip().lower() for name in lieux_be])
lieux_be


# In[8]:


def get_lieux(value, lieux):
    liste = []
    valeurs = str(value).strip().lower().replace("- ", "-")
    valeurs = re.sub(r"\s+", " ", valeurs).split(' ')


    for i, tokens in enumerate(valeurs):
        try:
            if tokens in lieux:
                tokens = tokens
            elif tokens + " " + valeurs[i+1] in lieux:
                tokens = tokens + " " + valeurs[i+1]
            elif tokens + "-" + valeurs[i+1] in lieux:
                tokens = tokens + "-" + valeurs[i+1]
            elif tokens + "-" + valeurs[i+1] + "-" + valeurs[i+2] in lieux:
                tokens = tokens + "-" + valeurs[i+1] + "-" + valeurs[i+2]
            elif tokens + " " + valeurs[i+1] + " " + valeurs[i+2] in lieux:
                tokens = tokens + " " + valeurs[i+1] + " " + valeurs[i+2]
            elif tokens + " " + valeurs[i+1] + " " + valeurs[i+2] + valeurs[i+3]in lieux:
                tokens = tokens + " " + valeurs[i+1] + " " + valeurs[i+2] + + valeurs[i+3]
            elif tokens + " " + valeurs[i+1] + " " + valeurs[i+2] + valeurs[i+3]in lieux:
                tokens = tokens + "-" + valeurs[i+1] + "-" + valeurs[i+2] + valeurs[i+3]
        except IndexError:
            pass
        if tokens in lieux:
            liste.append(tokens)

    
    liste = set(liste)
    return "||".join(liste)


# In[9]:

annot['extract_geonames'] = np.vectorize(get_lieux)(annot['queries'], lieux=lieux_be)
query = "select * from annot where length(extract_geonames) > 1"
pysql(query)


# In[123]:

with open(r"C:\Users\Boulot\Desktop\prenoms.tsv", 'r', encoding="utf8") as f:
    prenoms = set([name.strip().lower() for name in f])
prenoms


# In[122]:

with open(r"C:\Users\Boulot\Desktop\Names.tsv", 'r', encoding="utf8") as f:
    noms_famille = set([name.strip().lower() for name in f])
noms_famille


# In[82]:

def get_personnes(value):
    CHARS = "abcdefghijklmnopqrstuvwxyzéëèàäâçüûùABCDEFGHIJKLMNOPQRSTUVWXYZ- "
    
    family_joint = ["d'", "d", "de", "du", "der", "den", "vander", "vanden", "van", "le", "la"]
    
    valeurs = "".join(unidecode(c.lower().replace("-", " ")) for c in str(value) if c in CHARS).strip()
    valeurs = re.sub(r"\s+", " ", valeurs).split(' ')
    
    liste = []
    
    if len(valeurs) > 1:
        for i, token in enumerate(valeurs):
            if token in prenoms:
                liste.append(token)
                try:
                    liste.append(valeurs[i + 1])
                    if valeurs[i + 1] in family_joint and valeurs[i + 2] not in liste:
                        liste.append(valeurs[i + 2])
                        if valeurs[i + 2] in family_joint and valeurs[i + 3] not in liste:
                            liste.append(valeurs[i + 3])
                except IndexError:
                    try:
                        if valeurs[i - 1] not in liste:
                            liste.insert(1, valeurs[i - 1])
                            if valeurs[i - 2] in family_joint and valeurs[i - 2] not in liste:
                                liste.insert(1, valeurs[i - 2])
                            if valeurs[i - 3] in family_joint and valeurs[i - 3] not in liste:
                                liste.insert(1, valeurs[i - 3])
                    except IndexError:
                        pass
    
    #liste dédoublonnée
    seen = set()
    seen_add = seen.add
    liste = [x for x in liste if not (x in seen or seen_add(x))]
    return " ".join(liste)


# In[83]:

annot['extract_persons'] = np.vectorize(get_personnes)(annot['queries'])
query = "select * from annot where length(extract_persons) > 1"
pysql(query)


# In[110]:

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def get_wikipedia(value):
    for lang in ["fr", "nl", "en"]:
        wikipedia.set_lang(lang)
        try:
            w = wikipedia.page(value, auto_suggest=True)
            score= difflib.SequenceMatcher(None, value, re.sub(r"\(.+\)", "", w.title)).ratio()
            if score >= 0.7:
                return w.title + "||" + w.url + "||" + ":::".join(wikipedia.WikipediaPage(w.title).categories)
            elif score >= 0.5:
                return "Possibilité: " + w.title + "||" + w.url + "||" + ":::".join(wikipedia.WikipediaPage(w.title).categories)
        except wikipedia.exceptions.PageError:
            continue
        except wikipedia.exceptions.DisambiguationError as e:
            w = e.options[0]
            return w  + "||https://fr.wikipedia.org/wiki/" + w + " ::: ambigu "
    
print(get_wikipedia("charles michel"))


# In[98]:

query = "select * from annot where length(extract_persons) > 1"
df = pysql(query)
df


# In[108]:

start_time = time.time()
annot['wikipedia_person'] = annot['extract_persons'].apply(lambda x: get_wikipedia(x) if len(x)> 1 else None)
print("--- %s seconds ---" % (time.time() - start_time))


# In[111]:

start_time = time.time()
annot['wikipedia_lieux'] = annot['extract_geonames'].apply(lambda x: get_wikipedia(x) if len(x)> 1 else None)
print("--- %s seconds ---" % (time.time() - start_time))


# In[112]:

annot


# In[11]:

#fonction qui sert à splitter les colonnes multivaluées
def tidy_split(df, column, sep, keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df


# In[12]:

annot = tidy_split(annot, 'extract_geonames', sep='||')
annot


# In[13]:

def get_geonames(value):
    url = "http://api.geonames.org/searchJSON?" 
    
    payload = {"q":value,
            "maxRows":1,
            "country":"BE",
            "style":"full",
            "lang=":"FR",
            "username":"ettorerizza"}
    if len(value) >= 1:
        r = requests.get(url, params=payload)
    
        return r.json()["geonames"][0]["toponymName"]
    

#print(get_geonames("saint josse"))


# start_time = time.time()
# annot['json_geonames'] = np.vectorize(get_geonames)(annot['extract_geonames'])
# print("--- %s seconds ---" % (time.time() - start_time))

# query = "select * from annot where length(json_geonames) > 1"
# pysql(query)
# 

# In[14]:

print(annot.json_geonames[4])


# In[120]:

#ne pas utiliser pour l'instant
from SPARQLWrapper import SPARQLWrapper, JSON

def query(value, lang):
            value = value.title()
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            sparql.setQuery("""
            PREFIX schema: <http://schema.org/>
            SELECT DISTINCT ?item ?article ?itemDescription WHERE {
            ?item rdfs:label "%s"@%s.
            ?item wdt:P17 wd:Q31.
            ?article schema:about ?item.
            ?article schema:isPartOf <https://%s.wikipedia.org/>.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "%s". }
            }
            """ % (value, lang, lang, lang)) 
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            try:
                results_df = pd.io.json.json_normalize(results['results']['bindings'])
                resultats = results_df.iloc[0]['article.value']
            except IndexError:
                resultats = None
            return resultats

def get_sparql(value):
    if value is not None:
        try:
            resultats = query(value, "fr")
            if resultats is None:
                resultats = query(value, "nl")
                if resultats is None:
                    resultats = query(value, "en")
        except IndexError:
            resultats = None
        return resultats
    
#print(query("carnières", "fr"))


# In[116]:

start_time = time.time()
annot['wikidata_loc'] = annot['extract_geonames'].apply(lambda x: get_sparql(x) if len(x)> 1 else None)
print("--- %s seconds ---" % (time.time() - start_time))


# In[118]:

annot


# In[34]:

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
                       "exsentences":2,
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


def get_wikipedia_page(value):
    try:

        if type(value) is str:
            value = value.title()
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
                        elif ("belgique" in cat['title'].lower() or 
                              "plaats" in cat['title'].lower() or 
                              "municipali" in cat['title'].lower() or
                              "localité" in cat['title'].lower()):
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


# In[117]:

def get_wikipedia_element(ville):
    try:
        resp = get_wikipedia_page(ville)
        if resp == None:
            resp = get_wikipedia_page2(ville)
        (title, url, length, categories, extract, wikidata) = resp
        return title + ":::" + url + ":::" + extract + ":::" + wikidata + ":::" + str(length)
    except TypeError:
        pass
    
print(get_wikipedia_element("carniere")) 


# start_time = time.time()
# annot['wikipedia_loc'] = np.vectorize(get_wikipedia_element)(annot["extract_geonames"]) 
# print("--- %s seconds ---" % (time.time() - start_time))

# In[67]:

start_time = time.time()
annot['wikipedia_loc'] = annot['extract_geonames'].apply(lambda x: 0 if x is None else get_wikipedia_element(x))
print("--- %s seconds ---" % (time.time() - start_time))


# In[125]:

query = "select * from annot where length(extract_persons) > 1"
df = pysql(query)
df


# In[126]:

def compare_names(value):
    family_joint = ["d'", "d", "de", "du", "der", "den", "vander", "vanden", "van", "le", "la"]
    test = value.strip().lower().split(' ')
    print(test)
    try:
        name = test[-1]
        if test[-3] in family_joint:
            name = test[-3] + " " + test[-2] + " " + test[-1]
        elif test[-2] in family_joint:
            name = test[-2] + " " + test[-1]
    except IndexError:
        pass
    print(name)
    
    if name in noms_famille:
        return "Possible nom"
    else:
        return "Improbable"
    


# In[127]:

start_time = time.time()
annot['isName'] = annot['extract_persons'].apply(lambda x: compare_names(x) if len(x)> 1 else None)
print("--- %s seconds ---" % (time.time() - start_time))


# In[130]:

pysql("select extract_persons, isName from annot where length(extract_persons) > 1")


# In[ ]:

#annot.to_csv(r"C:\Users\Boulot\Desktop\test.csv", encoding='utf8')

