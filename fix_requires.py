#!/usr/bin/env python

renames = '''
backend/index.js -> backend/Backend.js
backend/bridge.js -> backend/Bridge.js
backend/compat-inject.js -> backend/compatInject.js
backend/make-compat.js -> backend/makeCompat.js
chrome/panel/index.js -> chrome/panel/Panel.js
frontend/container.js -> frontend/Container.js
frontend/context-menu.js -> frontend/ContextMenu.js
frontend/harness.js -> frontend/Harness.js
frontend/highlighter.js -> frontend/Highlighter.js
frontend/node.js -> frontend/Node.js
frontend/prop-state.js -> frontend/PropState.js
frontend/props.js -> frontend/Props.js
frontend/search-pane.js -> frontend/SearchPane.js
frontend/simple.js -> frontend/Simple.js
frontend/split-pane.js -> frontend/SplitPane.js
frontend/store.js -> frontend/Store.js
frontend/tree-view.js -> frontend/TreeView.js
frontend/data-view/index.js -> frontend/data-view/DataView.js
frontend/data-view/simple.js -> frontend/data-view/Simple.js
frontend/dir-to-dest.js -> frontend/dirToDest.js
frontend/node-matches-text.js -> frontend/nodeMatchesText.js
'''

renames = {source: dest
            for (source, dest) in
                [line.strip().split(' -> ')
                    for line in renames.split('\n')
                        if line.strip()]}

print renames

import os
import sys
import re
import pdb

dirs = sys.argv[1:]
state = {}

def fix_dep(dep):
    if dep[0] != '.':
        return None
    full = os.path.normpath(os.path.join(state['dir'], dep))
    hasIndex = False
    if full + '.js' not in renames:
        hasIndex = True
        full += '/index'
    full += '.js'
    if full not in renames:
        return None

    base = os.path.dirname(dep) if not hasIndex else dep
    ndep = os.path.join(base, os.path.basename(renames[full]))
    if ndep.endswith('.js'):
        ndep = ndep[:-len('.js')]
    print 'trade', dep, 'for', ndep
    #pdb.set_trace()
    return ndep

def fix_require(match):
    ndep = fix_dep(match.groupdict()['dep'])
    if not ndep:
        start, end = match.span()
        return match.string[start:end]
    return "require('{}')".format(ndep)

def fix_import(match):
    ndep = fix_dep(match.groupdict()['dep'])
    if not ndep:
        start, end = match.span()
        return match.string[start:end]
    return "from '{}'".format(ndep)

def fix(text):
    fixed = re.sub('''(require\((?P<quot>['"])(?P<dep>.*?)(?P=quot)\))''', fix_require, text)
    fixed = re.sub('''(from (?P<quot>['"])(?P<dep>.*?)(?P=quot))''', fix_import, fixed)
    return fixed

def awesome():
    for dir in dirs:
        files = os.listdir(dir)
        state['dir'] = dir
        for name in files:
            if name[0] == '.': continue
            full = os.path.join(dir, name)
            print 'in', full
            if os.path.isfile(full) and name.endswith('.js'):
                text = open(full).read()
                fixed = fix(text)
                open(full, 'w').write(fixed)

awesome()

# vim: et sw=4 sts=4
