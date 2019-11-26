from lxml import etree
from urllib.request import urlopen
import argparse
import random

def read_file(file_dir):
    links = []
    with open(file_dir, "r") as f:
        for link in f:
            item_link = link
            if link[-1] == '\n':
                item_link = item_link[:-1]
            links.append(item_link)
    return links

def generate(links, n):
    sentences = []

    while len(sentences) < n:
        link = links[random.randint(0, len(links) - 1)]
        try:
            fp = urlopen(link)
            page = fp.read().decode("utf8")
            dom = etree.HTML(page)

            paragraphs = dom.xpath('//article/p/text()')
            for paragraph in paragraphs:
                _sentences = paragraph.split('\n')
                for _sentence in _sentences:
                    __sentence = _sentence.split('.')
                    for tmp in __sentence:
                        if len(tmp) > 10:
                            sentences.append(tmp)
        except:
            print("[ERROR] Link :%s" % link)

    return sentences[:n]

def export_file(sentences, file_dir):
    with open(file_dir, "w") as f:
        for sentence in sentences:
            tmp = sentence
            if tmp[0] == ' ':
                tmp = tmp[1:]
            if tmp[-1] == ' ':
                tmp = tmp[:-1]
            f.write(tmp + "\n")

# python3 get_sentences.py vnexpress_article_links.txt sentences.txt 1000
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', type=str, help='directory of links file')
    parser.add_argument('output_dir', type=str, help='directory of sentences file')
    parser.add_argument('sentences', type=int, help='number of generated setences')
    args = parser.parse_args()

    links = read_file(args.input_dir)

    sentences = generate(links, args.sentences)
    export_file(sentences, args.output_dir)