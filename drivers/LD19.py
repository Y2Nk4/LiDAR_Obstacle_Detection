import math

import cv2
import serial
from helpers import calculate_crc
import numpy as np
from threading import Thread
from Video import Video

POINT_PER_PACK = 12
HEADER = 0x54
BYTES_PER_PACK = 47
BAUD_RATE=230400
MAX_RANGE = 6000
IMG_SIZE = 2000
CENTER = int(IMG_SIZE / 2)
MULTI_FACTOR = 2

class LD19:
    def __init__(self, serial_port, multi_factor=MULTI_FACTOR):
        self.multi_factor = multi_factor
        self.max_range = MAX_RANGE

        self.ser = serial.Serial(serial_port, baudrate=BAUD_RATE)
        self.points = np.zeros((360 * self.multi_factor, 2), np.uint16)

        self.counter = 0
        self.buffer = b''

    def to_hex(self, data):
        return ' '.join(format(x, '02x') for x in data)

    def parse_packet(self, data):
        # print(to_hex(data))
        if data[1] & 0x1F != POINT_PER_PACK:
            print("length does not match {}", data[1] & 0x1F)

        # Verify CRC8 checksum
        crc = calculate_crc(data[:-1])
        if crc != data[-1]:
            print(len(data))
            print("{} does not match with {}", (format(crc, '02x'), format(data[-1], '02x')))
            return

        start = int.from_bytes(data[4:6], byteorder="little")
        end = int.from_bytes(data[42:44], byteorder="little")

        diff = ((end + 36000) - start) % 36000
        step = diff / (POINT_PER_PACK - 1) / 100.0

        start = start / 100
        end = (end % 36000) / 100
        timestamp = int.from_bytes(data[44:46], byteorder="little")

        for i in range(POINT_PER_PACK):
            point_idx = 6 + i * 3
            angle = (start + step * i) % 360
            angle = angle if angle <= 360 else angle - 360
            mapped_angle = int(angle * self.multi_factor) % (360 * self.multi_factor)
            distance = int.from_bytes(data[point_idx:point_idx + 2], byteorder="little")
            confidence = data[point_idx+2]
            self.points[mapped_angle, 0] = distance
            self.points[mapped_angle, 1] = confidence

        self.counter = self.counter + 1
        if (self.counter % 50) == 0:
            self.counter = 0
            print(timestamp)

    def start(self):
        Thread(target=self.retrieve, args=()).start()
        return self

    def retrieve(self):
        while True:
            self.buffer += self.ser.read(self.ser.in_waiting)
            # print(to_hex(buffer))

            header_idx = self.buffer.find(HEADER)

            # header is not found
            if header_idx == -1:
                self.buffer = b''
                continue

            # packet is not finished
            if len(self.buffer[header_idx:]) < BYTES_PER_PACK:
                self.buffer = self.buffer[header_idx:]
                continue
            else:
                data = self.buffer[header_idx:header_idx+BYTES_PER_PACK]
                self.parse_packet(data)
                self.buffer = self.buffer[header_idx+BYTES_PER_PACK:]

