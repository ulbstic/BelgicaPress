# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:35:25 2017

@author: Boulot
"""

import pandas as pd
import numpy as np
import difflib

def fuzzy_match(a, b):
    left = '1' if pd.isnull(a) else a
    right = b.fillna('2')
    out = difflib.get_close_matches(left, right)
    return out[0] if out else np.NaN

df1 = pd.read_csv(r"C:\Users\Boulot\Desktop\BelgicaPress working dir\RESULTAT.csv", encoding="utf8")
df2 = pd.read_csv(r"C:\Users\Boulot\Desktop\BelgicaPress working dir\geonames_be.csv", encoding="utf8")

df1['extract_geonames'] = df1['extract_geonames'].astype(str)
df2['nom_officiel'] = df2['nom_officiel'].astype(str)


df1['geoname_clean'] = df1['extract_geonames'].apply(lambda x: fuzzy_match(x, df2['nom_officiel'])[0])
df1.merge(df2)