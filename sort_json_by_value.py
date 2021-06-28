import json

from collections import OrderedDict
from operator import itemgetter


def sort_json_by_value(fp):
    with open(fp, mode="r", encoding="utf-8") as file:
        d = json.load(file)
        d = OrderedDict(sorted(d.items(), key=itemgetter(1)))
    with open(fp, mode="w", encoding="utf-8") as file:
        json.dump(d, file, ensure_ascii=False, indent=2)

fp = "source_texts_trigram_count.json"
sort_json_by_value(fp)
