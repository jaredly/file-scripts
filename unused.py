#!/usr/bin/env python

import os
import sys
import re

BLACK = 'node_modules', 'build'

unused = set()
data = {}
users = {}
missing = {}

# dirs = sys.argv[1:]
# for dir in dirs:

def crawlDir(dir):
    files = os.listdir(dir)
    for name in files:
        full = os.path.join(dir, name)
        if os.path.isfile(full) and name.endswith('.js'):
            unused.add(full)
            data[full] = open(full).read()
            users[full] = set()
        elif os.path.isdir(full) and name not in BLACK:
          crawlDir(full)

list(crawlDir(name) for name in os.listdir('.') if os.path.isdir(name) and name not in BLACK)

for name in data:
    reqs = re.findall('''(require\((?P<quot>['"])(?P<dep>.*?)(?P=quot)\))''', data[name])
    for _, _, dep in reqs:
        if not dep or dep[0] != '.':
            # print 'package', dep
            continue
        rel = os.path.normpath(os.path.join(os.path.dirname(name), dep))
        if rel + '.js' not in data and (rel + '/index.js') in data:
            rel += '/index'
        if rel + '.js' not in users:
            if rel + '.js' not in missing:
                missing[rel + '.js'] = set()
            missing[rel + '.js'].add(name)
            continue
        users[rel + '.js'].add(name)
        if rel + '.js' in unused:
            unused.remove(rel + '.js')

print
print 'Unused:'
for name in sorted(unused):
    if '/webpack.' in name: continue
    print name

print
print 'Users:'
for name in sorted(users.keys()):
    if name in unused: continue
    print name, list(users[name])

print
print 'Missing:'
for name in sorted(missing.keys()):
    print name, list(missing[name])

# vim: et sw=4 sts=4
