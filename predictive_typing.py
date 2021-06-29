"""
To do: 
"""

import json
from collections import defaultdict, OrderedDict
from operator import itemgetter
import re

from openiti.helper.ara import normalize_ara_heavy
    

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

##def edge_n_grams(tokens, edge_d=defaultdict(lambda: defaultdict(list))):
##    """split tokens into character n-grams
##    (ch, cha, char, chara, ...) and return a dictionary of these
##    character n-grams with lists of their token n-grams"""
##    for t in tokens:
##        #print(t)
##        for i in range(2, len(t)):
##            #print("edge_d[{}][{}]".format(i, t[:i]))
##            #input()
##            edge_d[i][t[:i]].append(t)
##    return edge_d

def edge_n_grams(tokens, min_chars=5, normalize=normalize_ara_heavy):
    """split tokens into edge n-grams
    (i.e., character n-grams starting at the beginning of the token)
    with minimum length `min_chars` and maximum length
    the number of characters in the token.
    
    E.g., if the token is "character": "chara", "charac", "charact", ...
    Return a dictionary of these edge n-grams, in which the
    keys are the edge n-grams and the values a list of the remaining
    characters in the tokens that start with these edge n-grams.
    """
    edge_d = defaultdict(list)
    for t in tokens:
        #print(t)
        for i in range(min_chars, len(t)+1):
            if normalize:
                edge_d[normalize(t[:i])].append(t[i:])
            else:
                edge_d[t[:i]].append(t[i:])
    return edge_d

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
##    mono = edge_d[len(chars)][chars]
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
    

    #bi = edge_d_bi[chars]
    #d2 = {k:bigrams[k] for k in bi}
    tri = edge_d_tri[chars]
    d3 = {k:trigrams[k] for k in tri}
    #d = dict(d2.items() | d3.items())
    
    #print_sorted_dict(d)
    print_sorted_dict(d3)



fp = "source_texts_bigram_count.json"
bigrams = load_ngrams(fp)
fp = "source_texts_trigram_count.json"
trigrams = load_ngrams(fp)

edge_d_bi = edge_n_grams(bigrams)
with open("edge_ngrams_in_bigrams.json", mode="w", encoding="utf-8") as file:
    json.dump(edge_d_bi, file, ensure_ascii=False, indent=2)
with open("edge_ngrams_in_bigrams.json", mode="r", encoding="utf-8") as file:
    edge_d_bi = json.load(file)


edge_d_tri = edge_n_grams(trigrams)
with open("edge_ngrams_in_trigrams.json", mode="w", encoding="utf-8") as file:
    json.dump(edge_d_tri, file, ensure_ascii=False, indent=2)
with open("edge_ngrams_in_trigrams.json", mode="r", encoding="utf-8") as file:
    edge_d_tri = json.load(file)

chars = input("type some characters: ")
predict(chars)





