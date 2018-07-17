# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:55:22 2017

@author: Boulot
"""
from SPARQLWrapper import SPARQLWrapper, JSON


def get_wikidata(value):
  sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
  sparql.setQuery("""
  PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
  SELECT ?item ?label ?description ?score1 WHERE {
  ?item wdt:P17 wd:Q31.
  ?item rdfs:label ?label.
  ?item schema:description ?description.
  FILTER(EXISTS { ?item wdt:P625 ?x. })
  FILTER(CONTAINS(LCASE(STR(?label)), "%s"))
  FILTER(LANG(?label) = "fr").
  FILTER(LANG(?description) = "fr").
}
LIMIT 1 """ % value)

  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()

  for result in results["results"]["bindings"]:
    return result["label"]["value"] + "||" +  \
        result["item"]["value"] + "||" + result["description"]["value"]


print(get_wikidata("cathédrale de tournai"))
