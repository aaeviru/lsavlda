#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import math
import re
import numpy as np

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

a = np.load('/home/ec2-user/data/classinfo/vt.npy')#lsa result
kk = a.shape[0]

lsacr = {}

for root, dirs, files in os.walk(sys.argv[1]):
    for name in files:
        filename = root + '/' + name
        if filename[len(filename)-1] == 't':
            fin = open(filename,'r')
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
                cll.add(cl.group(2))
                clstart = clstart + cl.end(2)
                cl = re.search(r'(.*?)([A-H][0-9]+?[A-Z])',temp[clstart:clend],re.DOTALL)
            dv = np.zeros(kk)
            filename = filename + '.fq'
            fin = open(filename,'r')
            fin.readline()
            for line in fin:
                line = line.strip('\n')
                line = line.split()
                if line[1] in wtol:
                    dv = dv +  (int(line[0]) * a[:,wtol[line[1]]])
            #ids = dv.argsort()[::-1][:len(cll)]
            lsacl = dv.argmax()
            for cl in cll:
                if cl not in lsacr:      
                    lsacr[cl] = {}
                #for lsacl in ids:
                if lsacl in lsacr[cl]:
                    lsacr[cl][lsacl] = lsacr[cl][lsacl] + 1
                else:
                    lsacr[cl][lsacl] = 1
for cl in lsacr:
    dsum = 0
    dmax = 0
    lsaclmax = -1
    for lsacl in lsacr[cl]:
        dsum = dsum + lsacr[cl][lsacl]
        if lsacr[cl][lsacl] > dmax:
            dmax = lsacr[cl][lsacl]
            lsaclmax = lsacl
    print cl,lsaclmax,dmax,dsum

