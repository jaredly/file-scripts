#!/usr/bin/env python

import sys
import re

rx = re.compile('(?P<line>\d+):(?P<col>\d+)\s+(?P<level>\w+).+?(?P<type>[-\w]+)$')

def parse_rule(line):
  return rx.match(line.strip()).groupdict()

text = open(sys.argv[1]).read()
files = {}
block = {}
for line in text.split('\n'):
  if not line.strip():
    continue
  if ' problems ' in line:
    continue
  if line[0] != ' ':
    block = []
    files[line.strip()] = block
  else:
    block.append(parse_rule(line.strip()))

print block

for fname in files:
  lines = open(fname).read().split('\n')
  dirty = False
  for item in files[fname]:
    if item['type'] != 'semi':
      continue
    dirty = True
    lno = int(item['line']) - 1
    col = int(item['col'])
    line = lines[lno]
    lines[lno] = line[:col] + ';' + line[col:]
  if dirty:
    open(fname, 'w').write('\n'.join(lines))

# vim: et sw=4 sts=4
