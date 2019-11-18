from os import listdir
from os.path import isfile, join

paths = [join("subtitles", f) for f in listdir("subtitles") if isfile(join("subtitles", f)) and f.endswith(".srt")]


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

msgs = []
for p in paths:
    msgs += process(p)

print(len(msgs))
