import json
import re
import os

from openiti.helper.ara import normalize_ara_heavy

def normalized_key_map(d, n=None, normalize_f=normalize_ara_heavy):
    """create a dictionary with normalized keys from the given dictionary `d`
    in order to facilitate lookup of normalized keys.
    The function can also be used to update such a dictionary with normalized keys.

    Args:
        d (dict): the dictionary of which the keyse need to be normalized
        n (dict): a dictionary with normalized keys to which the counts in
            the `d` dictionary must be added
        normalize_f (function): the function to be used to normalize the keys
    """
    if not n:
        n = dict()
    for k, v in d.items():
        normalized_key = normalize_f(k)
        ## reduce size:
        #if k == normalized_key:
        #    k = "id"
        if normalized_key not in n:
            n[normalized_key] = {k: 0}
        if k not in n[normalized_key]:
            n[normalized_key][k] = 0
        n[normalized_key][k] += v
    return n

def normalize_keys_in_file(infp, outfp, normalize_f=normalize_ara_heavy):
    with open(infp, mode="r", encoding="utf-8") as file:
        d = json.load(file)
    n = normalized_key_map(d, normalize_f=normalize_f)
    with open(outfp, mode="w", encoding="utf-8") as file:
        json.dump(n, file, ensure_ascii=False, indent=2)

normalize_keys_in_file("source_texts_bigram_count.json",
                       "source_texts_bigrams_normalized_keys.json")
normalize_keys_in_file("source_texts_trigram_count.json",
                       "source_texts_trigrams_normalized_keys.json")

    
