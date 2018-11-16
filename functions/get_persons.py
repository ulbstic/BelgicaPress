# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from unidecode import unidecode
import re

with open(r"..\data\prenoms.txt", 'r', encoding="utf8") as f:
    prenoms = set([name.strip().lower() for name in f])
    
#with open(r"C:\Users\Boulot\Desktop\Names.tsv", 'r', encoding="utf8") as f:
#    noms = set([name.strip().lower() for name in f])

def get_personnes(value):
    CHARS = "abcdefghijklmnopqrstuvwxyzéëèàäâçüûùABCDEFGHIJKLMNOPQRSTUVWXYZ- "
    
    family_joint = ["d'", "d", "de", "du", "der", "den", "vander", "vanden", "van", "le", "la"]
    
    valeurs = "".join(unidecode(c.lower().replace("-", " ")) for c in value if c in CHARS).strip()
    valeurs = re.sub(r"\s+", " ", str(valeurs)).split(' ')
    
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

print(get_personnes("faust, camille laurent celestin (alias mauclair, camille ; 1872-1945)"))