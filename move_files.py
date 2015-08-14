#!/usr/bin/env python

import os
import sys
import re

dirs = sys.argv[1:]
unused = set()
data = {}
users = {}

lower = set()

def destName(text):
    exports = re.search('module\.exports\s*=\s*(\w+)', text)
    if not exports:
        return None
    return exports.groups()[0]

def pascamel(name, dest):
    if dest[0].isupper():
        name = name[0].upper() + name[1:]
    return re.sub('-(\w)', lambda m: m.groups()[0].upper(), name)

for dir in dirs:
    files = os.listdir(dir)
    for name in files:
        full = os.path.join(dir, name)
        if os.path.isfile(full) and name.endswith('.js'):
            text = open(full).read()
            dest = destName(text)
            if dest:
                dest = pascamel(name, dest)
                fulldest = os.path.join(dir, dest)
                print 'Moving', name, '\t\t', dest, fulldest
                if full != fulldest:
                    os.unlink(full)
                    open(fulldest, 'w').write(text)



# vim: et sw=4 sts=4
