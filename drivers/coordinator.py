from LD19 import LD19
from Video import Video
from ComputingUnit import ComputingUnit

if __name__ == '__main__':
    ld19 = LD19("/dev/tty.usbserial-0001", multi_factor=2)
    compute = ComputingUnit(raw_points=ld19.points,
                            multi_factor=ld19.multi_factor,
                            max_range=ld19.max_range, image_size=2000)
    video = Video(compute)

    ld19.start()
    video.start()