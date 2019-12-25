#!/usr/bin/env python3

from subprocess import Popen as cmd, PIPE
import sys
from bs4 import BeautifulSoup, NavigableString
from img2text import ocr
import re
from tqdm import tqdm
import os
path = os.path.dirname(os.path.abspath(__file__))

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

txt = cmd(f'{path}/trackID "{file}"', shell=True, executable='/usr/local/bin/zsh',stdout=PIPE).stdout.read().decode('utf8').strip()
print(txt)
if not txt.isdigit():
    print(f'No valid track was found in {file}')
    txt = cmd(f'mkvmerge -i {file}', shell=True, executable='/usr/local/bin/zsh',stdout=PIPE).stdout.read().decode('utf8').strip()
    txt = '\n'.join(x for x in txt.split('\n') if 'Track' in x)
    print(txt)
    exit()

cmd(f'ffmpeg -i "{file}" -map 0:{txt} -c copy {path}/out.sup', shell=True, executable='/usr/local/bin/zsh').wait()
cmd(f'mkdir out; java -jar {path}/BDSup2Sub.jar {path}/out.sup -o {path}/out/done.xml', shell=True, executable='/usr/local/bin/zsh').wait()
cmd(f'rm {path}/out.sup', shell=True, executable='/usr/local/bin/zsh').wait()
cmd(f'for f in {path}/out/*.png; do echo "$f"; convert "$f" -negate "${{f%.*}}.jpg"; rm "$f"; done', shell=True, executable='/usr/local/bin/zsh').wait()

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

cmd(f'rm -r {path}/out', shell=True, executable='/usr/local/bin/zsh').wait()