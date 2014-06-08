#!/usr/bin/python2.7
"""
Selector: A rinse.fm autodownloader

This script reads a config file, goes to the rinse website to look up the shows
in question, then downloads new shows to a directory specified in the config
file.
"""

from datetime import date
import os
import re
import urllib #TODO: requests
import yaml

CONFIG_FILE = "./config.yaml" #All the user has to bother with here

TRACK_RE = "http://[a-z/.]+/[a-zA-Z]+[0-9][0-9][0-9][0-9][0-9][0-9].mp3"
RINSE_URL = "http://rinse.fm/podcasts/?showID="

class Selector(object):
    """Handle parsing and downloading files.
    """
    def __init__(self, config_file=CONFIG_FILE):
        self.config = yaml.safe_load(open(config_file))

    def get_backlog(self):
        """
        Get a list of urls of shows that have not yet been downloaded.
        """
        dl_list = {} #{"dir1": ["url1", "url2"]}
        for name, info in self.config["shows"].iteritems():
            print("Show: " + name)
            all_eps = []

            f = urllib.urlopen(RINSE_URL + str(info["id"]))
            for line in f:
                if re.search(TRACK_RE, line):
                    all_eps.extend(re.findall(TRACK_RE, line))

            all_eps = set(all_eps)

            for ep in all_eps:
                if (get_url_date(ep) > info["last-dl"] or
                    info["last-dl"] == None):
                    if not name in dl_list:
                        dl_list[name] = []
                    print("Found new episode: " + ep)
                    dl_list[name].append(ep)

        return dl_list

    def download_shows(self, backlog):
        """
        Download specific shows from the suppied list.

        :param list backlog: A list of URLs to download.
        """
        for show, eps in backlog.items():
            for ep in eps:
                filename = ep.split("/")[-1]
                dest = os.path.join(self.config["directory"], filename)

                if "dir" in self.config["shows"][show]:
                    dest = os.path.join(self.config["directory"],
                        self.config["shows"][show]["dir"], filename)

                print("Downloading " + ep + " to " + dest)
                urllib.urlretrieve(ep, dest)

    def update_config(self):
        """
        Update last downloaded dates in the config file.
        """
        for info in self.config["shows"].values():
            info["last-dl"] = date.today()

        with open(CONFIG_FILE, "w") as f:
            f.write("%YAML 1.2\n---\n")
            yaml.dump(self.config, f, default_flow_style=False)

def get_url_date(url):
    """
    Get a date object from a rinse podcast url.
    """
    return date(2000 + int(url[-6:-4]), int(url[-8:-6]), int(url[-10:-8]))

def main():
    """
    Start the script.
    """
    selector = Selector()
    backlog = selector.get_backlog()

    if len(backlog) > 0:
        selector.download_shows(backlog)
        selector.update_config()

if __name__ == "__main__":
    main()

