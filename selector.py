#!/usr/bin/python2.7
"""
Selector: A rinse.fm autodownloader

This script reads a config file, goes to the rinse website to look up the shows
in question, then downloads new shows to a directory specified in the config
file.
"""

import os
import yaml
import urllib
import re
from datetime import date

CONFIG_FILE = "./config.yaml" #All the user has to bother with here
TRACK_RE = "http://[a-z/.]+/[a-zA-Z]+[0-9][0-9][0-9][0-9][0-9][0-9].mp3"
RINSE_URL = "http://rinse.fm/podcasts/?showID="
CONFIG = yaml.safe_load(open(CONFIG_FILE))

def get_url_date(url):
    """
    Get a date object from a rinse podcast url.
    """
    return date(2000 + int(url[-6:-4]), int(url[-8:-6]), int(url[-10:-8]))

def get_backlog():
    """
    Get a list of urls of shows that have not yet been downloaded.
    """
    dl = {} #{"dir1": ["url1", "url2"]}
    for name, info in CONFIG["shows"].iteritems():
        print("Show: " + name)
        all_eps = []
        f = urllib.urlopen(RINSE_URL + str(info["id"]))
        for line in f:
            if re.search(TRACK_RE, line):
                all_eps.extend(re.findall(TRACK_RE, line))
        all_eps = list(set(all_eps))
        for ep in all_eps:
            if get_url_date(ep) > info["last-dl"] or info["last-dl"] == None:
                if not name in dl:
                    dl[name] = []
                print("Found new episode: " + ep)
                dl[name].append(ep)
    return dl

def download_shows(backlog):
    """
    Download specific shows from a list.
    """
    for show, eps in backlog.items():
        for ep in eps:
            filename = ep.split("/")[-1]
            dest = os.path.join(CONFIG["directory"], filename)
            if "dir" in CONFIG["shows"][show]:
                dest = os.path.join(CONFIG["directory"],
                    CONFIG["shows"][show]["dir"], filename)
            print("Downloading " + ep + " to " + dest)
            urllib.urlretrieve(ep, dest)

def update_config():
    """
    Update last downloaded dates in the config file.
    """
    for info in CONFIG["shows"].values():
        info["last-dl"] = date.today()
    f = file(CONFIG_FILE, "w")
    f.write("%YAML 1.2\n---\n")
    yaml.dump(CONFIG, f, default_flow_style=False)

def main():
    backlog = get_backlog()
    if len(backlog) > 0:
        download_shows(backlog)
        update_config()

if __name__ == "__main__":
    main()
