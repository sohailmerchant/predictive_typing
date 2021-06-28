"""
To do: 
"""

import json
from collections import defaultdict, OrderedDict
from operator import itemgetter
import re


def load_ngrams(fp):
    with open(fp, mode="r", encoding="utf-8") as file:
        return json.load(file)

def sort_trigrams(d):
    el_1 = defaultdict(list)
    el_2 = defaultdict(list)
    #el_3 = defaultdict(list)
    for k in d:
        s = k.split(" ")
        el_1[s[0]].append(k)
        el_2[s[1]].append(k)
        #el_3[s[2]].append(k)
    return el_1, el_2   #, el_3

##def character_n_grams(tokens, char_d=defaultdict(lambda: defaultdict(list))):
##    """split tokens into character n-grams
##    (ch, cha, char, chara, ...) and return a dictionary of these
##    character n-grams with lists of their token n-grams"""
##    for t in tokens:
##        #print(t)
##        for i in range(2, len(t)):
##            #print("char_d[{}][{}]".format(i, t[:i]))
##            #input()
##            char_d[i][t[:i]].append(t)
##    return char_d

def character_n_grams(tokens):
    """split tokens into character n-grams
    (ch, cha, char, chara, ...) and return a dictionary of these
    character n-grams with lists of their token n-grams"""
    char_d = defaultdict(list)
    for t in tokens:
        #print(t)
        for i in range(2, len(t)):
            char_d[t[:i]].append(t)
    return char_d

def print_sorted_dict(d):
    def sort_key(e):
        """sort results first on number of occurrences, \
        then on length of the ngram"""
        return (e[1], len(e[0]))
    #d = OrderedDict(sorted(d.items(), key=itemgetter(1), reverse=True))
    d = OrderedDict(sorted(d.items(), key=sort_key, reverse=True))
    for k, v in d.items():
        print(v, k)

##def predict_before_one_word(chars):
##    mono = char_d[len(chars)][chars]
##    print(chars, "appear in", len(mono), "words")
##    tri = [el_1[m] for m in mono]
##    tri = [item for sublist in tri for item in sublist]
##    print(tri)
##    d = {k:trigrams[k] for k in tri}
##    bi = [" ".join(item.split(" ")[:2]) for item in tri]
##    print(bi)
##    print(len(d))
##    d.update({k:bigrams[k] for k in bi})
##              
##
##    #print_sorted_dict(d)
##    return d
##
##def predict_after_one_word(word):
##    tri = el_1[word]
##    d = {k:trigrams[k] for k in tri}
##    
##    #print_sorted_dict(d)
##    return d

##def combine_dicts(d1, d2):
##    for k, v in d2.items():
##        if k in d1:
##            d1[k] = d1[k] + d2[k]
##        for
##    return d1
    
def predict(chars):

    # normalize input:
    chars = re.sub("[^\w ]", "", chars)
    chars = " ".join(chars.strip().split(" ")[-2:])
    print(chars)
    

    #bi = char_d_bi[chars]
    #d2 = {k:bigrams[k] for k in bi}
    tri = char_d_tri[chars]
    d3 = {k:trigrams[k] for k in tri}
    #d = dict(d2.items() | d3.items())
    
    #print_sorted_dict(d)
    print_sorted_dict(d3)



fp = "source_texts_bigram_count.json"
bigrams = load_ngrams(fp)
fp = "source_texts_trigram_count.json"
trigrams = load_ngrams(fp)

##char_d_bi = character_n_grams(bigrams)
##with open("char_ngrams_in_bigrams.json", mode="w", encoding="utf-8") as file:
##    json.dump(char_d_bi, file, ensure_ascii=False, indent=2)
with open("char_ngrams_in_bigrams.json", mode="r", encoding="utf-8") as file:
    char_d_bi = json.load(file)


##char_d_tri = character_n_grams(trigrams)
##with open("char_ngrams_in_trigrams.json", mode="w", encoding="utf-8") as file:
##    json.dump(char_d_tri, file, ensure_ascii=False, indent=2)
with open("char_ngrams_in_trigrams.json", mode="r", encoding="utf-8") as file:
    char_d_tri = json.load(file)

chars = input("type some characters: ")
predict(chars)





