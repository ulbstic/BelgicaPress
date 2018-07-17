# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 09:59:55 2017

@author: Boulot
"""


import requests


def get_wikipedia_page2(value):

  if type(value) is str:
    value = value.title()
    for lang in ["fr", "nl", "en"]:

      url = "https://{}.wikipedia.org/w/api.php?".format(lang)

      payload = {"format": "json",
                 "action": "query",
                 "generator": "search",
                 "gsrnamespace": 0,
                 "gsrsearch": value,
                 "gsrlimit": 20,
                 "prop": "categories|extracts|info|revisions|pageprops",
                 "inprop": "url",
                 "ppprop": "wikibase_item",
                 "rvprop": "content",
                 "exintro": "",
                 "explaintext": "",
                 "exsentences": 2,
                 "exlimit": "max",
                 "cllimit": "max"}

      r = requests.get(url, params=payload).json()
      print(requests.get(url, params=payload).url)
      try:
        for pageid, page in r["query"]["pages"].items():
          try:
            if page['title'].startswith(value):
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
                    # page['revisions'])
                    return info
                    break

          except KeyError:
            continue

      except (KeyError, UnboundLocalError):
        return None


print(get_wikipedia_page2("Bruxelles"))


def get_wikipedia_element(ville):
  resp = get_wikipedia_page2(ville)
  if resp is None:
    return "not found"
  else:
    try:
      (title, url, length, categories, extract, wikidata) = resp
    except KeyError:
      pass
  return url


print(get_wikipedia_element("Bruxelles"))

#liste = []
# for c in communes:
#    liste.append(get_wikipedia_element(c.strip()))
# print(liste)
#
# with open(r"C:\Users\Boulot\Desktop\liste.tsv", "w") as f:
#    for i in liste:
#        f.write(i + "\n")
