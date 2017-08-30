# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 12:13:41 2017

@author: Boulot
"""
from SPARQLWrapper import SPARQLWrapper, JSON


def get_sparql(value):
    if value is not None:
        sparql = SPARQLWrapper("http://fr.dbpedia.org/sparql")
        sparql.setQuery("""
        SELECT DISTINCT ?entity ?score1 ?type
            WHERE{
                ?entity ?p ?label.
                ?entity ?q ?abstract.
                        Filter langMatches(lang(?label),"FR").
                        Filter langMatches(lang(?abstract),"FR").
                ?label <bif:contains> "'%s'" OPTION(score ?score1).
                ?abstract <bif:contains> "'commune'"
                FILTER (?p=<http://www.w3.org/2000/01/rdf-schema#label> ||
                        ?p=<http://www.w3.org/2004/02/skos/core#prefLabel>).
                FILTER (?q=<http://dbpedia.org/ontology/abstract>).
                ?entity a ?type.
                FILTER (?type IN (<http://dbpedia.org/ontology/Place>)).
                FILTER isIRI(?entity).
            } order by (?score1) LIMIT 3
        """ % (value) ) 
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        liste = []
        try:
            for result in results["results"]["bindings"]:
                liste.append(result['entity']['value'])
        except:
            pass

    return " ".join(liste)

print(get_sparql("wynendaele"))