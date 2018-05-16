# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 13:23:58 2017

@author: Boulot
"""
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

def query(value, lang):
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            sparql.setQuery("""
            PREFIX schema: <http://schema.org/>
            SELECT DISTINCT ?item ?article ?itemDescription WHERE {
            ?item rdfs:label ?itemLabel
            FILTER(CONTAINS(LCASE(?itemLabel), "%s"@%s)).
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
            resultats = query(value, "en")
            if resultats is None:
                resultats = query(value, "fr")
                if resultats is None:
                    resultats = query(value, "nl")
        except IndexError:
            resultats = None
        return resultats
            

print(get_sparql("houx"))

#print(query("Brussels", "en"))

print("merbes-sainte-marie".title())