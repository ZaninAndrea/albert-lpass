# -*- coding: utf-8 -*-

"""lpass wrapper extension"""

import subprocess as sp
from shutil import which
import subprocess
import re
from fuzzywuzzy import process, fuzz

from albertv0 import *

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "LastPass"
__version__ = "1.0"
__trigger__ = "lp"
__author__ = "Andrea Zanin"
__dependencies__ = ["lpass"]

cmd = __dependencies__[0]
if which(cmd) is None:
    raise Exception("'%s' is not in $PATH." % cmd)

iconPath = iconLookup("font")


out = subprocess.check_output(["lpass", "ls", "-l"])
lines = str(out).split("\\n")

regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} (.*) \[id: (.*)\] \[username: (.*)\]"

results = []
for line in lines:
    matches = re.finditer(regex, line, re.MULTILINE)
    for match in matches:
        name, id, username = match.groups()
        name = name.split("/")[-1]
        results.append((name, username, id))


def getBestMatches(query):
    ratios = [(result,
               max(
                   fuzz.partial_ratio(result[0], query),
                   fuzz.partial_ratio(result[1], query))
               )
              for result in results]
    ratios.sort(key=lambda ratio: ratio[1])
    ratios.reverse()
    best_ratios = [ratio for ratio in ratios[:4] if ratio[1] > 85]

    items = []
    for match in best_ratios:
        best_match = "username: %s site: %s" % (match[0][1], match[0][0])

        item = Item(
            id=__prettyname__,
            icon=iconPath,
            text=best_match,
            subtext="Copy password to clipboard",
            completion=best_match,
            actions=[ProcAction("Copy to clipboard", [
                                "lpass", "show", match[0][2], "--clip", "--password"])]
        )

        items.append(item)

    return items


def handleQuery(query):
    if query.isTriggered:
        return getBestMatches(query.string.strip())
