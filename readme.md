Selector
========

An autodownloader for rinse.fm podcasts.

Dependencies
------------

* [PyYAML](http://pyyaml.org/)

Installation
------------

`pip install PyYAML`

Use
---

1. Download the python script and the example `YAML` config file.
2. Rename `config.yaml.examle` to `config.yaml`.
3. Add shows you want to download to `config.yaml`. If you've downloaded them
before, you can put the date of the last show you downloaded for the last-dl
item.
4. You can put `config.yaml` anywhere you want, but if it's not in the
same directory as the script change `CONFIG_FILE` in `selector.py` to match its
path.

All done! Simply run selector.py whenever you want to check for and download
new shows. You can also run it in a cronjob weekly if you want:

    0    13    *    *    0  /path/to/selector

Will run `selector` at 13:00 every Sunday.