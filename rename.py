#!/usr/bin/env python3


import os
import sys
import re
import random
import string
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def most_similar(a, b):
    ascore = []
    for x in a:
        tmp = []
        for y in b:
            tmp.append((similar(x, y), x, y))
        ascore.append(max(tmp))
    return ascore

def jumbles():
    name = ''
    for i in range(random.randint(1, 2)):
        name += jumble(random.randint(1, 4)) + '.'
    return name

def jumble(num):
    return ''.join(random.choices(string.ascii_letters+string.digits, k=num))

simrename = False
testmode = False
srtChar = 'x'

args = sys.argv

if len(args) > 1:
    if 'E' in args:
        print('SRT format \'S01E23\'\n')
        srtChar = 'E'
    if 'e' in args:
        print('SRT format \'s01e23\'\n')
        srtChar = 'e'
    if 'movie' in args:
        simrename = True
    if 'test' in args:
        simrename = False
        testmode = True
if srtChar == 'x':
    print('SRT format \'01x23\'\n')
    


files = os.listdir()

vids = sorted([x for x in files if x[-3:].lower() in ('mkv', 'mp4', 'avi', 'm4v')])
subs = sorted([x for x in files if x[-3:] == 'srt'])
# print('vids', vids)
# print('subs', subs)
sims = most_similar(subs, vids)
for subgroup in sims:
    if testmode:
        pct = "{:.0%}".format(subgroup[0])
        print(subgroup[1], '\n\twas most similar (%s) to\n' % pct + subgroup[2])
        print()
    if simrename:
        os.rename(subgroup[1], subgroup[2][:-3]+'srt')
        print(subgroup[1])
        print('\twas renamed to')
        print(subgroup[2][:-3]+'srt')
        print()
print()



vidrgx = re.compile(r'[sS]\d+ ?[eE]\d+')

for x in vids:
    if vidrgx.search(x):
        ep = vidrgx.findall(x)[0][-2:]
        # print('x', x)
        # print('ep', ep)
        for sub in subs:
            if ep in sub and sub[sub.rfind(ep)-1] == srtChar:
                print(str(sub))
                if not testmode:
                    os.rename(str(sub), str(x)[:-3]+'srt')
                    print('\twas renamed to')
                else:
                    print('\twould be renamed to')
                print(str(x)[:-3]+'srt')
                print()


# print(os.getcwd())

# folder = './test/'
# for the_file in os.listdir(folder):
#     file_path = os.path.join(folder, the_file)
#     try:
#         if os.path.isfile(file_path):
#             os.unlink(file_path)
#         #elif os.path.isdir(file_path): shutil.rmtree(file_path)
#     except Exception as e:
#         print(e)

# for i in range(1, 5):
#     s1 = jumbles()
#     s2 = jumbles()
#     with open(os.path.join('test', s1+'S01E'+'%0*d' % (2, i)+'.'+s2+args[1]), 'w') as f:
#         f.write('')
#     with open(os.path.join('test', (s1+'01x'+'%0*d' % (2, i)+'.'+s2+'srt').replace('.', ' - ')), 'w') as f:
#         f.write('')

# os.rename('x.txt', 'x.txt'.replace('x', 'pineapple'))