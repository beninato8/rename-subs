from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def most_similar(a, b):
    ascore = []
    for x in a:
        tmp = []
        for y in b:
            tmp.append((similar(x, y), x, y))
        ascore.append(max(tmp)[1:])
    return ascore

srtlist = ['a S01E01.srt', 
          'b S01E02.srt', 
          'c S01E03.srt', 
          'd S01E04.srt', 
          'e S01E05.srt', 
          'f S01E06.srt', 
          'g S01E07.srt', 
          'h S01E08.srt', 
          'i S01E09.srt', 
          'j S01E10.srt']

vidlist = ['k S01E01.mkv', 
           'l S01E02.mkv', 
           'm S01E03.mkv', 
           'n S01E04.mkv', 
           'o S01E05.mkv', 
           'p S01E06.mkv', 
           'q S01E07.mkv', 
           'r S01E08.mkv', 
           's S01E09.mkv', 
           't S01E10.mkv']

print(most_similar(srtlist, vidlist))