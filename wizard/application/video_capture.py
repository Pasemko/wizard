import cv2 as cv
from wizard.configuration.constants import IMG_HEIGHT, IMG_WIDTH


class VideoCapture:
    def __init__(self, source=0):
        self.cap = cv.VideoCapture(source)
    

    def read(self):
        ret, frame = self.cap.read()
        frame = cv.flip(frame, 1)
        frame = cv.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
        return ret, frame
    
    
    def __del__(self):
        self.cap.release()
