import time
import numpy as np
import imageio
from pprint import pprint
from PIL import Image
import os

sourceDirectory = 'D:/BigDataChallenge/test'
hashes = dict()

def iterateOverFiles():
    global hashes
    directory = os.fsencode(sourceDirectory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        average = averageVideo(filename)
        hashes[filename[:-4]] = hashImage(average)

def averageVideo(filename):
    reader = imageio.get_reader(sourceDirectory + '/' + filename)
    average = None
    frames = 0
    for i, im in enumerate(reader):
        if average is None:
            average = np.zeros(im.shape)
        average += im
        frames += 1
    average = average / frames
    reader.close()
    return average

def hashImage(image):
    im = Image.fromarray(np.uint8(image))
    transformedImage = im.resize((8,9), Image.ANTIALIAS)
    transformedImage = transformedImage.convert("L")
    listOfColors = list(transformedImage.getdata())
    averageColor = sum(listOfColors) / len(listOfColors)
    bits = "".join(map(lambda pixelColor: '1' if pixelColor > averageColor else '0', listOfColors))
    hash = int(bits,2).__format__('016x').upper()
    return hash

if __name__ == '__main__':
    start_time = time.time()
    iterateOverFiles()
    pprint(hashes)
    pprint(len(hashes))
    print("Execution time: %s seconds." % (time.time() - start_time))