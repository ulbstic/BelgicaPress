# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 23:17:21 2017

@author: Boulot
"""

import wikipedia
import difflib
import warnings
import re
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
        

    
print(get_wikipedia("carnieres"))
