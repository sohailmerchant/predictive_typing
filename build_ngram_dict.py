"""
Build dictionaries of ngram counts.

The main() function builds a dictionary of edge ngrams
({<edge_ngram>: {<ngram>: <count>}})
for all texts in a folder.

Edge n-grams are character n-grams that start at the
beginning of a token.
For example, the token "character" is broken down into
the edge n-grams "c", "ch", "cha", "char", "chara", etc.
"""

import re
import os
from collections import defaultdict, deque, Counter
import json
from openiti.helper.ara import ar_tok, normalize_ara_heavy
from openiti.helper.funcs import get_all_text_files_in_folder
import time

def count_ngrams(s, n=2, token_regex=ar_tok, ngram_cnt=Counter()):
    """Count the different ngrams in string `s`.

    Args:
        t (str): string in which the ngrams must be counted
        n (int): number of tokens in each ngram
        token_regex (str): regular expression that defines a token
        ngram_cnt (obj): collections.Counter() object

    Returns:
        tuple (dict (key: ngram, val: count),
               str (last n-1 tokens in the string)) 
    """
    #ngram_cnt = Counter()
    toks = deque([None]*n, maxlen=n)
    #print(s)
    for m in re.finditer(token_regex, s):
        toks.append(m.group())
        #print(toks)
        #print(" ".join([t for t in toks if t]))
        
        try:
            ngram = " ".join(toks)  # will fail if toks still contains None value
            ngram_cnt[ngram] += 1
        except:
            continue
    toks.append(None)
    last_n_minus_one = " ".join([t for t in toks if t])
    #print("last_n_minus_one:", last_n_minus_one)
    #input("CONTINUE?")
    return ngram_cnt, last_n_minus_one

def count_ngrams_in_file(fp, outfp, n=2, header_splitter=None,
                         token_regex=ar_tok,
                         overwrite=False,
                         verbose=False,
                         across_paragraphs=False):
    """Count distinct ngrams in the body of a text file\
    and save the count as a json file at `outfp`.

    Args:
        fp (str): path to the text file
        outfp (str): path to the output file
        header_splitter (str): string that indicates the boundary
            between a metadata header and the body text;
            if None, tokens will be counted from the start of the file
        outfolder (str): path to the folder where the output json file
            will be stored
        token_regex (str): regular expression to describe a single token
        overwrite (bool): if False, count data will be loaded from existing
            json file. If True, existing json files will be overwritten.
        across_paragraphs (bool): if False, the script will not consider
            ngrams that straddle two paragraphs. Defaults to False.

    Returns:
        collections.Counter object ({<ngram>: <count>})
    """
    print("counting {}-grams...".format(n))
    start = time.time()
    if overwrite or not os.path.exists(outfp):
        fc = Counter()
        with open(fp, mode="r", encoding="utf-8") as file:
            # start counting only after the header,
            #if a header_splitter is defined:
            start_counting = True
            if header_splitter:
                start_counting = False
            
            para = ""
            prev = ""
            line = ""
            i = 0
            while True:
                line = file.readline()
                i += 1
                if not line:
                    break
                if not start_counting:  # line still in header
                    if header_splitter in line:
                        start_counting = True
                else:
                    if not across_paragraphs: 
                        if line.startswith("#"):
                            if para.strip():
                                #print(len(para))
                                count_ngrams(para, n=n, ngram_cnt=fc,
                                             token_regex=token_regex)
                                #r = input("Print para? Y/N")
                                #if r.lower() == "y":
                                #    print(para)
                                #    print(json.dumps(pc, ensure_ascii=False, indent=2))
                                para = line
                        else:
                            para += " " + line
                    else:
                        if len(para) > 1000:
                            _, prev = count_ngrams(para, n=n, ngram_cnt=fc,
                                                   token_regex=token_regex)
                            para = prev + " " + line
                        else:
                            para += " " + line
                            
                        
                if verbose:
                    if not i%10000:
                        print(i, len(fc))
        # add ngrams from last paragraph:
        count_ngrams(para, n=n, ngram_cnt=fc, token_regex=token_regex)
        if verbose:
            print(i, "lines")
            print("counting ngrams in {} took {} seconds".format(outfn, time.time()-start))
        with open(outfp, mode="w", encoding="utf-8") as file:
            json.dump(dict(fc), file, ensure_ascii=False, indent=2)
    else:
        with open(outfp, mode="r", encoding="utf-8") as file:
            fc = Counter(json.load(file))
        if verbose:
            print("loading ngram count from {} took {} seconds".format(outfn, time.time()-start))
    return fc

def join_ngram_counts(folder, outfp, fn_regex=".", 
                      input_threshold=1, output_threshold=1):
    """Join all ngram count json files inside a folder\
    including only keys that have a minimum value of `threshold`

    Args:
        folder (str): path to the folder containg the json files
        outfp (str): path to the file in which the compound count
            will be stored.
        input_threshold (int): only include an ngram from a text
            if that ngram has a count of at least `input_threshold`
            in that file.
        output_threshold (int): only include an ngram in the compound file
            if that ngram has a count of at least `output_threshold`
            in the compound dictionary count.
        
    Returns:
        collections.Counter object ({<ngram>: <count>})
    """
    cnt = Counter()
    print("COMBINING NGRAM COUNTS FROM BOOK JSONS:")
    print("(fn regex:", fn_regex, ")")
    fns = [fn for fn in os.listdir(folder) if re.findall(fn_regex, fn)]
    for fn in fns:
        print("-", fn)
        fp = os.path.join(folder, fn)
        with open(fp, mode="r", encoding="utf-8") as file:
            d = json.load(file)
            #d = {k:v for k,v in d.items() if v >= input_threshold}
            cnt += Counter(d)
    #cnt = {k:v for k,v in cnt.items() if v >= output_threshold}
    with open(outfp, mode="w", encoding="utf-8") as file:
        json.dump(cnt, file, ensure_ascii=False, indent=2)

    return cnt
        

def count_ngrams_in_folder(folder, outfp, temp_folder="TEMP",
                           n=2, header_splitter=None,
                           token_regex=ar_tok,
                           overwrite=False,
                           input_threshold=1,
                           output_threshold=1,
                           across_paragraphs=False
                           ):
    """Count distinct ngrams in the body of all text files in `folder`\
    and save the count as a json file in `outfp`.

    Args:
        fp (str): path to the text file
        outfp (str): path to the output file
        header_splitter (str): string that indicates the boundary
            between a metadata header and the body text;
            if None, tokens will be counted from the start of the file
        token_regex (str): regular expression to describe a single token
        overwrite (bool): if False, count data will be loaded from existing
            json file. If True, existing json files will be overwritten.
        input_threshold (int): only include an ngram from a text
            if that ngram has a count of at least `input_threshold`
            in that file.
        output_threshold (int): only include an ngram in the compound file
            if that ngram has a count of at least `output_threshold`
            in the compound dictionary count.

    Returns:
        collections.Counter object ({<ngram>: <count>})
    """
    if not os.path.exists(temp_folder):
        new_folder = True
        os.makedirs(temp_folder)
    else:
        new_folder = False
    temp_fns = []
    for fp in get_all_text_files_in_folder(folder):
        print(os.path.basename(fp))
        fn = os.path.splitext(os.path.basename(fp))[0]
        temp_fn = "{}_{}gram_count.json".format(fn, n)
        temp_fns.append(temp_fn)
        temp_fp = os.path.join(temp_folder, temp_fn)
        count_ngrams_in_file(fp, temp_fp, n=n, header_splitter=header_splitter,
                             token_regex=token_regex,
                             overwrite=overwrite,
                             across_paragraphs=across_paragraphs)
    outfn = os.path.basename(folder)
    if new_folder:
        fn_regex = "."
    else:
        fn_regex = "|".join(temp_fns)
    cnt = join_ngram_counts(temp_folder, outfp,
                            fn_regex=fn_regex, 
                            input_threshold=input_threshold,
                            output_threshold=output_threshold)

    return cnt

def create_edge_ngrams_d(d, edges_d=None, min_chars=5, 
                         normalize_f=normalize_ara_heavy,
                         excl_edge_from_ngram=False):
    """Create an edge ngram dictionary from ngram count dict `d`

    Args:
        d (dict): ngram count dictionary (key: ngram, value: count)
        edges_d (dict): edge ngram dictionary
            {<edge_ngram>: {<ngram>: <count>}}.
            If set to None, a new edge ngram dictionary will be created;
            if an edge ngram dictionary is provided, it will be updated
            with the new ngrams and counts from `d`
        min_chars (int): minimum number of characters for the edge n-grams
            (including spaces)
        edges_d (dict): if None, a new edge n-gram dictionary will be
            created; if a dictionary is provided, that one will be updated
            with the ngrams and counts from the dictionary at `infp`
        normalize_f (function): a function to be used to normalize
            the edge n-grams. If None, no normalization will be done.
        excl_edge_from_ngram (bool): if True, the first part of the
            ngram that is covered by the edge ngram will be removed
            from the dictionary to save space.

    Returns:
        dict ({<edge_ngram>: {<ngram>: <count>}})
        
    """
    if not edges_d:
        edges_d = dict()
    print("    keys in new dict d:", len(d))
    print("    keys in edges dict before:", len(edges_d))
    print("    excl_edge_from_ngram:", excl_edge_from_ngram)
    for k, v in d.items():
        if normalize_f:
            normalized_key = normalize_f(k)
        else:
            normalized_key = k
        for i in range(min_chars, len(normalized_key)+1):
            edge = normalized_key[:i]
            ## make dictionary smaller:
            if excl_edge_from_ngram:
                k = k[i:]
            if edge not in edges_d:
                edges_d[edge] = {k: 0}
            if k not in edges_d[edge]:
                edges_d[edge][k] = 0
            edges_d[edge][k] += v
    print("    keys in edges dict after:", len(edges_d))
    return edges_d

def create_edge_ngrams_d_from_file(infp, outfp=None, min_chars=5, edges_d=None,
                                   normalize_f=normalize_ara_heavy,
                                   excl_edge_from_ngram=False):
    """Create an edge ngram dictionary from ngram count dict at `infp`

    Args:
        infp (str): path to the input json file
        outfp (str): path to the output json file (if None,
            the dictionary will not be saved)
        min_chars (int): minimum number of characters for the edge n-grams
            (including spaces)
        edges_d (dict): edge ngram dictionary
            {<edge_ngram>: {<ngram>: <count>}}.
            If set to None, a new edge ngram dictionary will be created;
            if an edge ngram dictionary is provided, it will be updated
            with the new ngrams and counts from the dictionary at `infp`
        normalize_f (function): a function to be used to normalize
            the edge n-grams. If None, no normalization will be done.
        excl_edge_from_ngram (bool): if True, the first part of the
            ngram that is covered by the edge ngram will be removed
            from the dictionary to save space.

    Returns:
        dict ({<edge_ngram>: {<ngram>: <count>}})
    """
    with open(infp, mode="r", encoding="utf-8") as file:
        d = json.load(file)
    edges_d = create_edge_ngrams_d(d, edges_d=edges_d, normalize_f=normalize_f,
                                   excl_edge_from_ngram=excl_edge_from_ngram)
    if outfp:
        with open(outfp, mode="w", encoding="utf-8") as file:
            json.dump(edges_d, file, ensure_ascii=False, indent=2)
    return edges_d


def create_merged_edge_ngram_dict(folder, outfp, fn_regex=".",
                                  min_chars=5, 
                                  normalize_f=normalize_ara_heavy,
                                  excl_edge_from_ngram=False):
    """Create an edge ngram dictionary from selected \
    ngram count dictionaries in `folder`

    Args:
        folder (str): path to the folder containing the OpenITI texts
        outfp (str): path to the output json file
        fn_regex (str): regular expression that defines file names
            that should be merged
        min_chars (int): minimum number of characters for the edge n-grams
            (including spaces)
        normalize_f (function): a function to be used to normalize
            the edge n-grams. If None, no normalization will be done.
        excl_edge_from_ngram (bool): if True, the first part of the
            ngram that is covered by the edge ngram will be removed
            from the dictionary to save space.

    Returns:
        dict ({<edge_ngram>: {<ngram>: <count>}})
    """
    print("merging count dicts in folder", folder)
    d = dict()
    fns = [fn for fn in os.listdir(folder) if re.findall(fn_regex, fn)]
    for fn in fns:
        fp = os.path.join(folder, fn)
        print("  -", fp)
        d = create_edge_ngrams_d_from_file(fp, min_chars=min_chars,
                                           edges_d=d, outfp=None,
                                           normalize_f=normalize_f,
                                           excl_edge_from_ngram=excl_edge_from_ngram)
        print(len(d))
    with open(outfp, mode="w", encoding="utf-8") as file:
        json.dump(d, file, ensure_ascii=False)#, indent=2)

    return d
        
        
def main(folder, outfp, n=[2,3], temp_folder="TEMP", 
         header_splitter="#META#Header#End",token_regex=ar_tok,
         input_threshold=1, output_threshold=1,
         min_chars=5, normalize_f=normalize_ara_heavy,
         across_paragraphs=False, excl_edge_from_ngram=False,
         overwrite=False):
    """Build a dictionary of edge ngrams ({<edge_ngram>: {<ngram>: <count>}})
    for all OpenITI texts in `folder`


    Args:
        folder (str): path to the folder containing the OpenITI texts
        outfp (str): path to the output json file
        n (list or int): the number of tokens in the n-gram
            (provide a list if you want to include more than one n-gram type)
        temp_folder (str): path to the folder where intermediary files
            will be saved
        header_splitter (str): regex for the metadata header of the text files
            (text before this splitter will not be converted into n-grams)
        token_regex (str): regular expression that defines a token
        input_threshold (int): only include an ngram from a text
            if that ngram has a count of at least `input_threshold`
            in that file.
        output_threshold (int): only include an ngram in the output
            if that ngram has a count of at least `output_threshold`
            in the compound dictionary count.
        min_chars (int): minimum number of characters for the edge n-grams
            (including spaces)
        normalize_f (function): a function to be used to normalize
            the edge n-grams. If None, no normalization will be done.
        across_paragraphs (bool): if False, the script will not consider
            ngrams that straddle two paragraphs. Defaults to False.
        excl_edge_from_ngram (bool): if True, the first part of the
            ngram that is covered by the edge ngram will be removed
            from the dictionary to save space.
        overwrite (bool): if False, count data will be loaded from existing
            json file. If True, existing json files will be overwritten.

    Returns:
        dict ({<edge_ngram>: {<ngram>: <count>}})
    """
    try:
        n[0]
    except:
        n = [n]
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    for i in n:
        temp_fp = "{}/{}_{}gram_count.json".format(temp_folder, folder, i)
        count_ngrams_in_folder(folder, temp_fp, n=i,
                               header_splitter="#META#Header#End",
                               temp_folder=temp_folder,
                               token_regex=ar_tok,
                               overwrite=overwrite,
                               across_paragraphs=across_paragraphs
                               )
    d = create_merged_edge_ngram_dict(temp_folder, outfp,
                                      fn_regex=folder,
                                      normalize_f=normalize_f,
                                      excl_edge_from_ngram=excl_edge_from_ngram)
    return d
        
        
if __name__ == "__main__":
    folder = r"source_texts"
    outfp = "ngram_count_normalized_keys.json"
    main(folder, outfp, n=[2,3], header_splitter="#META#Header#End",
         temp_folder="TEMP", token_regex=ar_tok,
         input_threshold=1, output_threshold=1,
         normalize_f=normalize_ara_heavy,
         overwrite=True, across_paragraphs=True,
         excl_edge_from_ngram=True)
