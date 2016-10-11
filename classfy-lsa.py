#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re

if len(sys.argv) != 2:
    print "input:patent-folder"
    sys.exit(1)

fwl = open("/home/ec2-user/git/statresult/wordslist_dsw.txt","r")
wtol = {}
itow = {}
i = 0
for line in fwl:
    line = line.strip('\n')
    wtol[line] = i
    itow[i] = line
    i = i + 1
fwl.close()

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if filename[len(filename)-1] == 't':
            fin = open(filename,'r')
            print filename
            cll = set()
            temp = fin.read()
            fin.close()
            cl = re.search(r'(【国際特許分類第.*版】.*?)([A-H][0-9]+?[A-Z])',temp,re.DOTALL)
            cll.add(cl.group(2))
            clend = re.search(r'【ＦＩ】',temp)
            if clend != None:
                clend = clend.end()
            else:
                clend = cl.end()+300
            clstart = cl.end(2)
            cl = re.search(r'(.*?)([A-H][0-9]+?[A-Z])',temp[clstart:clend],re.DOTALL)
            check = 0
            while cl != None:
                if cl.group(2) in cll:
                    check = 1

                cll.add(cl.group(2))
                clstart = clstart + cl.end(2)
                cl = re.search(r'(.*?)([A-H][0-9]+?[A-Z])',temp[clstart:clend],re.DOTALL)
            for cl in cll:
                print cl
            if check == 1:
                raw_input()

