from LD19 import LD19
from Video import Video

if __name__ == '__main__':
    ld19 = LD19("/dev/tty.usbserial-0001")
    ld19.retrieve()