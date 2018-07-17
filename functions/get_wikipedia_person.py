# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 23:17:21 2017

@author: Boulot
"""

import wikipedia
from fuzzywuzzy import fuzz
import warnings
import re
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def get_wikipedia(value):
    liste = []
    for lang in ["fr"]:
        wikipedia.set_lang(lang)
        try:
            w = wikipedia.page(value)

            score = fuzz.ratio(value, w.title)
            print(score)
            if score >= 90:
                print(score)
                liste.append("Probable: " + w.title + "||" + w.url + "||" +
                             ":::".join(wikipedia.WikipediaPage(w.title).categories))
            elif score >= 50:
                liste.append("Possibilité: " + w.title + "||" + w.url + "||" +
                             ":::".join(wikipedia.WikipediaPage(w.title).categories))
            else:
                liste.append("Improbable: " + w.title + "||" + w.url + "||" +
                             ":::".join(wikipedia.WikipediaPage(w.title).categories))
        except wikipedia.exceptions.PageError:
            continue
        except wikipedia.exceptions.DisambiguationError as e:
            w = e.options[0]
            return w + "||https://fr.wikipedia.org/wiki/" + w + " ::: ambigu "
    return liste


print(get_wikipedia("ru de la loi"))
