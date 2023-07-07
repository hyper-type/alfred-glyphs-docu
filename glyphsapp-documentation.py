"""
Author: Mark Frömberg (https://markfromberg.com) :: @Mark2Mark
Published by: Hypertype (https://hypertype.xyz) :: @hyper-type

Script Filter Settings:

(Triggered by typing 'gd' followed by a space and filter query)
Keyword:   `gd`,                        check "with Space",     "Argument Optional"
Language:  `/bin/zsh` or `/bin/bash`,   "with input as argv"
Script:    `python3 glyphsapp-documentation.py "$1"`
"""

import urllib.request
import sys
import json
import re


def compare(a, b):
    if a.lower() in b.lower():
        return True
    return False


documentation_url = "https://docu.glyphsapp.com/"

# Fetch documentation and parse links
with urllib.request.urlopen(documentation_url) as response:
    html_content = response.read().decode("utf-8")

link_pattern = r'<dt id="([\w\.]+)">'  # alternatively for other sites: e.g. `r'<a href="#([\w\.]+)">'`
links = re.findall(link_pattern, html_content)

# Prepare the results as Alfred JSON
results = []
for link in links:
    result = {
        "uid": link,
        "title": link,
        "arg": documentation_url + "#" + link,
        "icon": {"path": "icon.png"},  # ripped from twitter
    }
    results.append(result)

# Filter results based on user input
query = sys.argv[1].strip()
if query:
    results = [result for result in results if compare(query, result["title"])]

# Output results as Alfred JSON
alfred_output = {"items": results}

sys.stdout.write(json.dumps(alfred_output))  # or use `print`
