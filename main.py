import time
import numpy as np
import imageio
from pprint import pprint
from PIL import Image

def averageVideo(videoUrl):
    reader = imageio.get_reader(videoUrl)
    average = None
    frames = 0
    for i, im in enumerate(reader):
        if average is None:
            average = np.zeros(im.shape)
        average += im
        frames += 1
    average = average / frames
    return average

def hashImage(image):
    im = Image.fromarray(np.uint8(image))
    transformedImage = im.resize((8,9), Image.ANTIALIAS)
    transformedImage = transformedImage.convert("L")
    listOfColors = list(transformedImage.getdata())
    averageColor = sum(listOfColors) / len(listOfColors)
    bits = "".join(map(lambda pixelColor: '1' if pixelColor > averageColor else '0', listOfColors))
    hash = int(bits,2).__format__('016x').upper()
    pprint(hash)

if __name__ == '__main__':
    start_time = time.time()
    average = averageVideo('D:/BigDataChallenge/videos/00SXM76KD1X2.mp4')
    hashImage(average)
    print("Execution time: %s seconds." % (time.time() - start_time))