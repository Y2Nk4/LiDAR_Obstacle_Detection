from threading import Thread
import numpy as np
import math
import cv2

IMG_SIZE = 1000
RADIAN_CONV = math.pi / 180

def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=3,
          font_thickness=2,
          text_color=(0, 255, 0),
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, (x-5,y-5), (x + text_w+5, y + text_h+5), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size

class ComputingUnit:
    def __init__(self, raw_points, multi_factor, max_range, image_size=IMG_SIZE):
        self.raw_points = raw_points
        self.multi_factor = multi_factor
        self.image_size = image_size
        self.center = self.image_size // 2
        self.max_range = max_range
        self.img = np.zeros((image_size, image_size, 3), np.uint8)


    def compute(self):
        self.img[:, :, :] = 0

        min_distance = np.min(self.raw_points[:, 0])
        pos = (20, 30)
        show_txt = "Minimum Distance: %.1f cm" % (min_distance / 10)

        for i in range(self.raw_points.shape[0]):
            (distance, confidence) = self.raw_points[i]
            angle = i / 2

            show_distance = distance / self.max_range * (self.image_size)

            color = (255, 0, 0)
            line_color = (0, 125, 125)
            if distance <= (min_distance+30):
                color = (0, 0, 255)
                line_color = (0, 0, 255)

            radian = angle * RADIAN_CONV

            x = int(show_distance * math.cos(radian) + (self.center))
            y = int(show_distance * math.sin(radian) + (self.center))

            cv2.line(self.img, (self.center, self.center), (x, y), line_color, 2)
            cv2.circle(self.img, (x, y), 2, color, 2)

        cv2.circle(self.img, (self.center, self.center), 2, (0, 255, 0), 4)
        draw_text(self.img, show_txt, pos=pos, font_scale=2, font_thickness=3, text_color=(255,0,0), text_color_bg=(255,255,255))
