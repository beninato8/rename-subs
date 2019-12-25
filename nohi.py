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

if any(x in content for x in blacklist):
    rgx = '|'.join(blacklist)
    content = re.sub(rgx, '', content)

# content = re.sub(r'\n[ -]+', r'\n', content)

# print(content)
with open(args[1], 'w') as f:
    f.write(content)