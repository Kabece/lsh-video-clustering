import multiprocessing
import os
import time
from pprint import pprint

import imageio
import numpy as np
from PIL import Image
from leven import levenshtein
from sklearn.cluster import dbscan

sourceDirectory = 'C:/BigDataChallenge/videos'
hashes = dict()
data = []


def iterateOverFiles():
    global hashes
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    directory = os.fsencode(sourceDirectory)
    for tuple in pool.imap(averageVideo, os.listdir(directory)):
        hashes[tuple[0]] = tuple[1]
        data.append(tuple[0])

def averageVideo(file):
    filename = os.fsdecode(file)
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
    return (hashImage(average), filename[:-4])

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
    return dbscan(X, metric=levenshteinMetric, eps=5, min_samples=2, n_jobs=-1)

def interpretClusters(clusters):
    global data, hashes
    interpretedClusters = [None]*970
    unclustered = set()
    for i, item in enumerate(clusters[1]):
        if item != -1:
            if interpretedClusters[item] is None:
                interpretedClusters[item] = set()
            interpretedClusters[item].add(hashes[data[i]])
        else:
            unclustered.add(hashes[data[i]])
    interpretedClusters[len(interpretedClusters) - 1] = unclustered
    return interpretedClusters

if __name__ == '__main__':
    start_time = time.time()
    iterateOverFiles()
    clusters = clusterImages()
    interpretedClusters = interpretClusters(clusters)
    pprint(interpretedClusters)
    print("Execution time: %s seconds." % (time.time() - start_time))