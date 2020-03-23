#!/usr/bin/env python3

from subprocess import Popen, PIPE
import sys
from bs4 import BeautifulSoup, NavigableString
from img2text import ocr
import re
from tqdm import tqdm
import os
path = os.path.dirname(os.path.abspath(__file__))

def remove_tmp_files():
    shell(f'rm -r {path}/out')
    shell(f'rm {path}/out.sup')

def shell(cmd):
    out, err = Popen(cmd, shell=True, executable='/usr/local/bin/zsh', stdout=PIPE).communicate()
    return out.decode('utf8').strip()

def clean(txt):
    txt = re.sub(r'\|', 'I', txt)
    return txt

#https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
def rreplace(s):
    li = s.rsplit(':', 1)
    return ','.join(li)

args = sys.argv
# args = [1, 'vid.mkv']
if len(args) < 2:
    print("Needs at least one argument")
    exit()

file = args[1]

txt = shell(f'{path}/trackID "{file}"')
print(txt)
if not txt.isdigit():
    print(f'No valid track was found in {file}')
    txt = shell(f'mkvmerge -i {file}')
    txt = '\n'.join(x for x in txt.split('\n') if 'Track' in x)
    print(txt)
    exit()

remove_tmp_files()
shell(f'ffmpeg -i "{file}" -map 0:{txt} -c copy {path}/out.sup')
shell(f'mkdir {path}/out; java -jar {path}/BDSup2Sub.jar {path}/out.sup -o {path}/out/done.xml')
shell(f'for f in {path}/out/*.png; do echo "$f"; convert "$f" -negate "${{f%.*}}.jpg"; rm "$f"; done')

with open(f'{path}/out/done.xml', 'r') as f:
    soup = BeautifulSoup(f, 'lxml')

soup = soup.findAll('events')[1]
# print(soup.prettify())

out = ''
i = 1
soup = [x for x in soup if not isinstance(x, NavigableString)]
for event in tqdm(soup):
    if not isinstance(event, NavigableString):
        out += f'{i}\n'
        start = rreplace(event['intc'])
        stop = rreplace(event['outtc'])
        out += f'{start} --> {stop}\n'
        img = event.find('graphic').contents[0].split('.')[0]
        txt = ocr(f'{path}/out/{img}.jpg')
        txt = clean(txt)
        out += txt + '\n\n'
        i += 1
        # exit()

with open(file.replace('.mkv', '.srt'), 'w+') as f:
    f.write(out)

remove_tmp_files()