"""
Selector: A rinse.fm autodownloader

This script reads a config file, goes to the rinse website to look up the shows
in question, then downloads new shows to a directory specified in the config
file.
"""

import yaml
import urllib
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
    """
    Get a list of urls of shows that have not yet been downloaded.
    """
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
            if(get_url_date(ep) > info["last-dl"] || info["last-dl"] == None):
                print("Found new episode: " + ep)
                dl.append(ep);
    return dl

def download_shows(backlog):
    """
    Download specific shows from a list.
    """
    global conf
    for ep in backlog:
        filename = ep.split("/")[-1]
        print("Downloading " + filename + " to " + conf["directory"])
        urllib.urlretrieve(ep, conf["directory"] + filename)

def update_config():
    """
    Update last downloaded dates in the config file.
    """
    global conf
    for name, info in conf["shows"].iteritems():
        info["last-dl"] = date.today()
    f = file(config_file, "w")
    f.write("%YAML 1.2\n---")
    yaml.dump(conf, f, default_flow_style=False)

def main():
    global conf;
    conf = open_config()
    backlog = get_backlog()
    if(len(backlog) > 0):
        download_shows(backlog)
        update_config()

if __name__ == "__main__":
    main()