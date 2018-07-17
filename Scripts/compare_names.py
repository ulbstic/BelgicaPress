# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:43:04 2017

@author: Boulot
"""

with open(r"C:\Users\Boulot\Desktop\Names.tsv", 'r', encoding="utf8") as f:
    noms_famille = set([name.strip().lower() for name in f])


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
        return "OK"
    else:
        return "Pas OK"
    
compare_names("diamond london")
        
        
    