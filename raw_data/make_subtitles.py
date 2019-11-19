from os import listdir
from os.path import isfile, join
import os
DIR = join(os.path.dirname(os.path.realpath(__file__)), "subtitles")

paths = [join(DIR, f) for f in listdir(DIR) if isfile(join(DIR, f)) and f.endswith(".srt")]

def process(path):
    f = open(path, "r")
    text = f.read()
    x = text.split("\n\n")[1:]
    res = []
    for x in x:
        xx = x.split("\n")
        if len(xx) < 3:
            continue
        res += xx[2:]
    return res

def get_all_texts():
    msgs = []
    for p in paths:
        msgs += process(p)
    return msgs
