#Things this should do:
#1. Read a config file to see what shows to download and when the last show downloaded was
#2. Go to rinse website for each of the shows
#3. Download all undownloaded episodes

import yaml
import urllib
import sys
import re
from datetime import date

config_file = "./config.yaml"
conf = []
track_re = "http://[a-z/.]+/[a-zA-Z]+[0-9][0-9][0-9][0-9][0-9][0-9].mp3"
rinse_url = "http://rinse.fm/podcasts/?showID="

def open_config():
    """
    Load the pyyaml config file.
    """
    global config_file
    return yaml.safe_load(open(config_file))

def get_url_date(url):
    """
    Get a date object from a rinse podcast url.
    """
    year = 2000 + int(url[-6:-4])
    month = int(url[-8:-6])
    day = int(url[-10:-8])
    return date(year, month, day)

def get_backlog():
    global conf
    dl = []
    print conf["shows"]
    for name, info in conf["shows"].iteritems():
        print("Show: " + name)
        all_eps = [];
        f = urllib.urlopen(rinse_url + str(info["id"]))
        for line in f:
            if re.search(track_re, line):
                all_eps.extend(re.findall(track_re, line))
        all_eps = list(set(all_eps))
        for ep in all_eps:
            if(get_url_date(ep) > info["last-dl"]):
                print("Found new episode: " + ep)
                dl.append(ep);
    return dl

def download_shows(backlog):
    global conf
    for ep in backlog:
        filename = ep.split("/")[-1]
        print("Downloading " + filename + " to " + conf["directory"])
        urllib.urlretrieve(ep, conf["directory"] + filename)

def update_config():
    global conf
    for name, info in conf["shows"].iteritems():
        info["last-dl"] = date.today()
    f = file(config_file, "w")
    yaml.dump(conf, f, default_flow_style=False)

def main(argv):
    global conf;
    conf = open_config()
    backlog = get_backlog()
    if(len(backlog) > 0):
        download_shows(backlog)
        update_config()

if __name__ == "__main__":
    main(sys.argv)