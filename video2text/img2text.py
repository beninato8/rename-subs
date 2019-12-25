import pytesseract
from PIL import Image
import sys

def ocr(img, psm=6):
    return pytesseract.image_to_string(Image.open(img), config=f'--psm {psm}')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("Needs at least one argument")
        exit()

    img = args[1]
    # print(ocr(img))
    i1 = 'out/done_0007.jpg'
    i2 = 'out/done_0008.jpg'
    for i in range(3, 14):
        print(i)
        print('****7****')
        print(ocr(i1, psm=i))
        print('****8****')
        print(ocr(i2, psm=i))