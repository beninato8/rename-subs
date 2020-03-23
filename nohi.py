#!/usr/bin/env python3

import sys
import re

args = sys.argv

if len(args) != 2:
    print('Only enter one file')
    exit()

try:
    with open(args[1], 'r') as f:
        content = f.read()
except Exception as e:
    with open(args[1], 'r', encoding='latin-1') as f:
        content = f.read()


blacklist = {'Sk0r', 'yomoy', 'Collioure', 'Feygnasse Team', 'La Fabrique', 'mpm', 'Jarick', 'do_Ob', 'The Ni.Knight', r'mkvcage\.com', 'Encoded by Hunter', 'Crazy4TV.com'}

content = re.sub(r'pos\(.*\)', r'', content)

content = re.sub(r'([\[\(].*\n?.*[\]\)] ?)|([^\d\n]+: ?)|([{}]+)', r'', content)
content = re.sub(r'{.+}', r'', content)
content = re.sub(r'{?[aA][nN]\d+}?', r'', content)
content = re.sub(r'[ ]{2,}', r' ', content)
content = re.sub(r'.*[\[\]].*', r'', content)
content = re.sub(r'{|}', r'', content)
content = re.sub(r'<[^>]*>', r'', content)
content = re.sub(r"'’", r"'", content)
content = re.sub(r"’", r"'", content)
content = re.sub(r'"', r"'", content)
content = re.sub(r"(?<=[^\d]):(?=[^\d])", r"", content)
content = re.sub(r"\*", r"", content)
content = re.sub(r"&quot;", r'"', content)
content = re.sub(r"([^\d]+):\n?", r'', content)
content = re.sub(r"(?<=[^\w])i(?=[^\w])", r'I', content)

# title
words = ['jedi', 'lothal', 'hera', 'ezra', 'imperial', 'wookies', 'vizago', 'r2', 'd2', 'zeb', 'kanan', 'lasan', 'lasat', 'senator organa', 'phantom', 'sabine']
cap = {x:x.title() for x in words}
for k,v in cap.items():
    content = re.sub(fr'(?<=[^\w]){k}(?=[^\w])', v, content)

# upper
words = ['c-3po', 'c3-po', 'c3po']
cap = {x:x.upper() for x in words}
for k,v in cap.items():
    content = re.sub(fr'(?<=[^\w]){k}(?=[^\w])', v, content)

if any(x in content for x in blacklist):
    rgx = '|'.join(blacklist)
    content = re.sub(rgx, '', content)

# content = re.sub(r'\n[ -]+', r'\n', content)

# print(content)
with open(args[1], 'w') as f:
    f.write(content)