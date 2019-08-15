#!/usr/bin/env python3
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="+")

args = parser.parse_args()

for filename in args.file:
    content = open(filename).read()
    m_begin = re.search(r"\\begin *{ *thebibliography *} *{ *[0-9]+ *}", content)
    m_end = re.search(r"\\end *{ *thebibliography *}", content)
    if m_begin is None or m_end is None:
        continue
    bibliography = content[m_begin.end():m_end.start()]
    bibitems = {}
    prev = bibliography.find(r"\bibitem")
    while prev != len(bibliography):
        cur = bibliography.find(r"\bibitem", prev + 1)
        if cur == -1: cur = len(bibliography)
        bibitem = bibliography[prev:cur].strip()
        print(prev, cur, bibitem)
        key = re.search(r"\\bibitem *{ *([^} ]+) *}", bibitem)
        assert key
        bibitems[key.group(1)] = bibitem
        prev = cur

    cites = []
    for c in re.findall(r"\\cite *{ *([^} ]+) *}", content):
        cites += [x.strip() for x in c.split(",")]


    unique_cites = []
    for c in cites:
        if c in unique_cites: continue
        unique_cites.append(c)
    
    new_content = content[:m_begin.end()] + "\n\n" + "\n".join([bibitems[c] + "\n" for c in unique_cites]) + "\n" + content[m_end.start():]
    open(filename + ".bak", "w").write(content)
    open(filename, "w").write(new_content)
