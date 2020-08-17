#!/usr/bin/env python3

import sys
import re
from pprint import pprint

args = sys.argv
# args += ['input.srt']

if len(args) != 2:
    print('Only enter one file')
    exit()

print(args[1])

try:
    with open(args[1], 'r') as f:
        input_srt = f.read()
except Exception as e:
    with open(args[1], 'r', encoding='latin-1') as f:
        input_srt = f.read()

class Section():
    def __init__(self, *lines):
        try:
            self.num = str(lines[0])
            self.time = str(lines[1])
            self.text = '\n'.join(lines[2:])
        except Exception as e:
            print(lines)
            raise e

    def clean(self):
        debug = False
        if self.num == '12300':
            debug = True
        content = self.text

        blacklist = {}
        content = re.sub(r'{\\an\d+}', r'', content)
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
        content = re.sub(r"\*", r"", content)
        content = re.sub(r"&quot;", r'"', content)
        content = re.sub(r".*: *", r'', content)
        content = re.sub(r"(?<=[^\w])i(?=[^\w])", r'I', content)
        content = re.sub(r'\n[-](?=\n)', r'', content)
        content = re.sub(r'^-\n', r'', content) # hypen at start of line
        content = re.sub(r'-[\s]*$', r'', content) # hyphen at end of line
        if debug:
            print(content)

        if any(x in content for x in blacklist):
            rgx = '|'.join(blacklist)
            content = re.sub(rgx, '', content)

        content = content.strip().rstrip()

        content = re.sub(r'\n+', r'\n', content)

        self.text = content

    def __str__(self):
        return '\n'.join([self.num, self.time, self.text])

cleaned = []
for x in input_srt.split('\n\n'):
    if x != '':
        sec = Section(*x.split('\n'))
        sec.clean()
        cleaned.append(str(sec))

# print('\n\n'.join(cleaned))

# exit()

with open(args[1], 'w') as f:
    f.write('\n\n'.join(cleaned))