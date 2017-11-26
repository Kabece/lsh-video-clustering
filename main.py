import time
import numpy as np
import imageio
from pprint import pprint

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

if __name__ == '__main__':
    start_time = time.time()
    averageVideo('D:/BigDataChallenge/videos/00SXM76KD1X2.mp4')
    print("Execution time: %s seconds." % (time.time() - start_time))