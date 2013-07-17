Selector
========

An autodownloader for rinse.fm podcasts.

Use
---

In order to set up selector, first download the python script and the example
yaml config file to your computer. Then, add shows you want to download to
config.yaml. If you've downloaded them before, you can put the date of the last
show you downloaded for the last-dl item. You can put this file anywhere you
want; just be sure to change the line in selector.py that points to it if it's
not in the same directory as the script.

After that, simply run selector.py whenever you want to check for and download
new shows. You can also run it in a cronjob weekly if you want:

    0    13    *    *    0  /path/to/selector

Will run selector at 13:00 every Sunday.