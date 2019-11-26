from urllib.request import urlopen
from xml.etree.ElementTree import parse

def parse_xml(sitemap_url):
    file = urlopen(sitemap_url)
    return parse(file)

year_sitemaps = []
for year in range(2001, 2020):
    year_sitemaps.append("https://vnexpress.net/articles-%d-sitemap.xml" % year)

links = []
f = open("vnexpress_article_links.txt", "w")
for sitemap_url in year_sitemaps:
    print("[PROCESSING] %s" % sitemap_url)
    tree = parse_xml(sitemap_url)
    root = tree.getroot()

    date_sitemaps = []
    for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        date_sitemaps.append(sitemap.text)

    for date_sitemap in date_sitemaps:
        try:
            tree = parse_xml(date_sitemap)
        except:
            print(date_sitemap)
        root = tree.getroot()
        for link in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            f.write(link.text + "\n")
            links.append(link.text)

    print("[DONE] %s, No. of Links: %d" % (sitemap_url, len(links)))
f.close()