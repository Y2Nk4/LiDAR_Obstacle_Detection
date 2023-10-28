from threading import Thread
import cv2

class Video:
    def __init__(self, compute=None):
        self.compute = compute
        self.stopped = False

    def start(self):
        self.show()
        return self

    def show(self):
        while not self.stopped:
            self.compute.compute()
            cv2.imshow('image', self.compute.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stopped = True

    def stop(self):
        self.stopped = True