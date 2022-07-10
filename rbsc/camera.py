import cv2
from cv2 import CV_8UC3
import numpy as np
from datetime import datetime

class Image:
    def __init__(self, src):
        self.src = cv2.VideoCapture(src) 
        self.last = self.frame

    def __getattr__(self, name):
        try:
            data = Image.Data(self.last)
            return data.__getattribute__(name)
        except:
            raise AttributeError(name)

    def __bytes__(self):
        _, jpeg = cv2.imencode('.jpg', self.last)
        return jpeg.tobytes()

    def __del__(self):
        self.src.release()
    
    def read(self):
        _ = self.frame
    
    @property
    def frame(self):
        _, self.last =  self.src.read()
        return self.last
    
    @property
    def data(self):
        return Image.Data(self.last)
    
    @staticmethod
    def cvt_color(color, cvt=cv2.COLOR_BGR2HSV):
        return cv2.cvtColor(np.uint8([[color]]), cvt)[0, 0]

    @staticmethod
    def video_write(name, shape, framerate):
        out = cv2.VideoWriter(name ,cv2.VideoWriter_fourcc('M','J','P','G'), fps=framerate, frameSize=shape)
        return out
    
    class Data:
        def __init__(self, frame, *crop):
            self.frame = frame
            self.shape = np.array(np.shape(self.frame)[-2::-1])
            self.center = self.shape //2

        def __bytes__(self):
            _, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
        
        def __call__(self, *crop):
            if len(crop) != 2:
                return self
            return Image.Data(self.crop(*crop))

        @property
        def light(self, cvt=cv2.COLOR_BGR2GRAY):
            return np.average(cv2.cvtColor(self.frame, cvt)) 

        def filter(self, *range, colors=([0]*3, [255]*3)):
            if len(range) != 2:
                raise Exception(f'Range must be 2 tuples')

            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            lo, hi = (np.array(color) for color in range)

            mask = cv2.inRange(hsv, lo, hi)
            w, h = self.shape

            filtered = np.empty((h, w, 3), 'uint8')
            filtered[mask == 0] = colors[0] 
            filtered[mask != 0] = colors[1] 

            # frame = self.frame.copy() 
            # frame[mask > 0] = (0, 255, 0)

            return Image.Data(filtered)
        
        def resize(self, size):
            frame = self.frame.copy()
            return cv2.resize(frame, size)
        
        @property
        def hsv(self):
            return cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        def save(self, path, name=None, format='.jpg'):
            if path[-1] != '/':
                path += '/'
            if not name:
                name=datetime.now()

            cv2.imwrite(path+str(name)+format, self.frame)
    
        def crop(self, center, shape):
            w, h = shape
            x = center[0] - (w // 2)
            y = center[1] - (h // 2)
            return self.frame[y:y+h, x:x+w]

        def dominant_colors(self, cnt):
            shape = Image.shape(self.frame)
            data = np.reshape(self.frame, (np.prod(shape), 3))
            data = np.float32(data)

            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS

            centers = cv2.kmeans(data, cnt, None, criteria, 10, flags)[2]
            return [tuple(int(val) for val in center) for center in centers]

        def draw_label(self, label, **style):
            if 'fontFace' not in style:
                style['fontFace'] = cv2.FONT_HERSHEY_SIMPLEX
            if 'thickness' not in style:
                style['thickness'] = 1
            if 'scale' in style:
                style['fontScale'] = style['scale'] 
                del style['scale']
            if not isinstance(label, str) :
                label = str(label)

            cv2.putText(self.frame, label, **style)

        def draw_limits(self, **style):
            start = (0, 0)
            end = self.shape - (1, 1)
            cv2.rectangle(self.frame, start, end, **style)
            cv2.circle(self.frame, end//2, radius=1, **style)

    @staticmethod
    def vboard(*imgs):
        concat = cv2.vconcat([imgs[0], imgs[1]])
        return concat

class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (255, 0, 0)
    green = (0, 255, 0)
    red = (0, 0, 255)
    cyan = (255, 255 ,0)
    magenta = (255, 0, 255)
    yellow = (0, 255, 255)

    def __init__(self, *vals, format='bgr'):
        self.format = format
        self.vals = {key:vals[ii] for ii, key in enumerate(format)}

    def __getattr__(self, *name):
        vals = []
        for char in name:
            if char not in self.format:
                return []
            vals.append(self.vals[char])
        return vals