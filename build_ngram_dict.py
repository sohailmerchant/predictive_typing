import re
import os
from collections import defaultdict, deque, Counter
import json
from openiti.helper.ara import ar_tok
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

def count_ngrams_in_file(fp, n=2, header_splitter=None,
                         outfolder="ngrams_in_texts",
                         token_regex=ar_tok,
                         overwrite=False,
                         verbose=False,
                         across_paragraphs=False):
    """Count distinct ngrams in the body of a text file\
    and save the count as a json file in `outfolder`.

    Args:
        fp (str): path to the text file
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
        collections.Counter object
    """
    start = time.time()
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outfn = os.path.splitext(os.path.basename(fp))[0]
    outfp = os.path.join(outfolder, outfn+"_ngram_count.json")
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

def join_ngram_counts(folder, outfp="total_counts.json",
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
        
    """
    cnt = Counter()
    print("COMBINING COUNTS FROM BOOK JSONS:")
    for fn in os.listdir(folder):
        print("-", fn)
        fp = os.path.join(folder, fn)
        with open(fp, mode="r", encoding="utf-8") as file:
            d = json.load(file)
            #d = {k:v for k,v in d.items() if v >= input_threshold}
            cnt += Counter(d)
    #cnt = {k:v for k,v in cnt.items() if v >= output_threshold}
    with open(outfp, mode="w", encoding="utf-8") as file:
        json.dump(cnt, file, ensure_ascii=False, indent=2)
    
        

def count_ngrams_in_folder(folder, n=2, header_splitter=None,
                           outfolder="ngrams_in_texts",
                           token_regex=ar_tok,
                           overwrite=False,
                           input_threshold=1,
                           output_threshold=1,
                           across_paragraphs=False
                           ):
    """Count distinct ngrams in the body of a text file\
    and save the count as a json file in `outfolder`.

    Args:
        fp (str): path to the text file
        header_splitter (str): string that indicates the boundary
            between a metadata header and the body text;
            if None, tokens will be counted from the start of the file
        outfolder (str): path to the folder where the output json file
            will be stored
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
        collections.Counter object
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    for fp in get_all_text_files_in_folder(folder):
        print(os.path.basename(fp))
        count_ngrams_in_file(fp, n=n, header_splitter=header_splitter,
                             outfolder=outfolder, token_regex=token_regex,
                             overwrite=overwrite, across_paragraphs=across_paragraphs)
    outfn = os.path.basename(folder)
    join_ngram_counts(outfolder, outfp=outfn+"_ngram_count.json",
                      input_threshold=input_threshold,
                      output_threshold=output_threshold)


folder = r"source_texts"
outfolder = r"trigrams"
count_ngrams_in_folder(folder, n=3,
                       header_splitter="#META#Header#End",
                       outfolder=outfolder,
                       token_regex=ar_tok,
                       overwrite=True,
                       across_paragraphs=True
                       )
        
