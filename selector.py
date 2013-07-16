#Things this should do:
#1. Read a config file to see what shows to download and when the last show downloaded was
#2. Go to rinse website for each of the shows
#3. Download all undownloaded episodes

import yaml
import urllib
import sys
import re

config_file = "./config.yaml"
track_re = "http://[a-z/.]+/[a-zA-Z]+[0-9][0-9][0-9][0-9][0-9][0-9].mp3"


def open_config():
    global config_file
    return yaml.safe_load(open(config_file))

def get_date(url):
    return url[-10:-4]

def get_backlog(conf):
    dl = []
    for show in conf:
        all_eps = [];
        f = urllib.urlopen("http://rinse.fm/podcasts/?showID=" +
            str(show["id"]))
        for line in f:
            if re.search(track_re, line):
                all_eps.extend(re.findall(track_re, line))
        all_eps = list(set(all_eps))
        for ep in all_eps:
            if(get_date(ep)): #if the date on the ep is earlier than the last dl

def main(argv):
    conf = open_config()
    get_backlog(conf)

if __name__ == "__main__":
    main(sys.argv)