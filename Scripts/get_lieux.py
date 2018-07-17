# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 11:31:29 2017

@author: Boulot
"""
import pandas as pd
import re


df = pd.read_csv(r"C:\Users\Boulot\Desktop\geonames_be_cleaned.csv", encoding="utf8")
lieux = df.noms


lieux = set([name.strip().lower() for name in lieux])

def get_lieux(value, lieux):
    liste = []
    valeurs = str(value).strip().lower().replace("- ", "-")
    valeurs = re.sub(r"\s+", " ", valeurs).split(' ')


    for i, tokens in enumerate(valeurs):
        try:
            if tokens in lieux:
                tokens = tokens
            if tokens + " " + valeurs[i+1] in lieux:
                tokens = tokens + " " + valeurs[i+1]
            if tokens + "-" + valeurs[i+1] in lieux:
                tokens = tokens + "-" + valeurs[i+1]
            if tokens + "-" + valeurs[i+1] + "-" + valeurs[i+2] in lieux:
                tokens = tokens + "-" + valeurs[i+1] + "-" + valeurs[i+2]
            if tokens + " " + valeurs[i+1] + " " + valeurs[i+2] in lieux:
                tokens = tokens + " " + valeurs[i+1] + " " + valeurs[i+2]
            if tokens + " " + valeurs[i+1] + " " + valeurs[i+2] + valeurs[i+3]in lieux:
                tokens = tokens + " " + valeurs[i+1] + " " + valeurs[i+2] + + valeurs[i+3]
            if tokens + " " + valeurs[i+1] + " " + valeurs[i+2] + valeurs[i+3]in lieux:
                tokens = tokens + "-" + valeurs[i+1] + "-" + valeurs[i+2] + valeurs[i+3]
        except IndexError:
            pass
        if tokens in lieux:
            liste.append(tokens)
        for i, tokens in enumerate(liste):
            try:
                if liste[i+1] in liste[i]:
                    del liste[i+1]
            except IndexError:
                pass


    
    liste = set(liste)
    return "||".join(liste)

print (get_lieux("la louvière", lieux))
