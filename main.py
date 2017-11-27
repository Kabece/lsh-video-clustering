import os
import time
from pprint import pprint

import imageio
import numpy as np
from PIL import Image
from leven import levenshtein
from sklearn.cluster import dbscan

sourceDirectory = 'C:/BigDataChallenge/test'
hashes = dict()
data = []

def iterateOverFiles():
    global hashes
    directory = os.fsencode(sourceDirectory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        average = averageVideo(filename)
        hashedImage = hashImage(average)
        hashes[filename[:-4]] = hashedImage
        data.append(hashedImage)

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

def levenshteinMetric(x, y):
    global data
    i, j = int(x[0]), int(y[0])
    return levenshtein(data[i], data[j])

def clusterImages():
    global data
    X = np.arange(len(data)).reshape(-1,1)
    pprint(X)
    clusters = dbscan(X, metric=levenshteinMetric, eps=5, min_samples=2)
    pprint(clusters)

if __name__ == '__main__':
    start_time = time.time()
    iterateOverFiles()
    clusterImages()
    print("Execution time: %s seconds." % (time.time() - start_time))