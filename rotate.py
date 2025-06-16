import cv2
import math
import base64
import numpy as np

class Rotate:
    def __init__(self, coarse_step=1, fine_step=0.1, radius_offset=5):
        self.coarse_step = coarse_step
        self.fine_step = fine_step
        self.radius_offset = radius_offset

    def rotate(self, img, angle, interp=cv2.INTER_LINEAR, border=cv2.BORDER_REFLECT):
        h, w = img.shape[:2]
        ctr = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(ctr, angle, 1)
        return cv2.warpAffine(img, M, (w, h), flags=interp, borderMode=border)

    def circle_ring(self, img, step, r):
        h, w = img.shape[:2]
        cx, cy = w // 2, h // 2
        pts = []
        for a in np.arange(0, 360, step):
            rad = math.radians(a)
            x = int(round(cx + r * math.cos(rad)))
            y = int(round(cy + r * math.sin(rad)))
            if 0 <= x < w and 0 <= y < h:
                pts.append(img[y, x])
            else:
                pts.append([0, 0, 0])
        return np.array(pts)

    def hsv_dist(self, c1, c2):
        dh = min(abs(int(c1[0])-int(c2[0])), 180-abs(int(c1[0])-int(c2[0]))) / 180
        ds = abs(int(c1[1]) - int(c2[1])) / 255
        dv = abs(int(c1[2]) - int(c2[2])) / 255
        return math.sqrt(dh*dh + ds*ds + dv*dv)

    def dev_sum(self, ring1, ring2):
        return np.sum([self.hsv_dist(i, o) for i, o in zip(ring1, ring2)])

    def best_angle(self, img1, img2):
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        r = img1.shape[0] // 2
        min_dev, best = float('inf'), 0
        for a in np.arange(0, 180, self.coarse_step):
            rot1 = self.rotate(hsv1, -a)
            rot2 = self.rotate(hsv2, a)
            ring1 = self.circle_ring(rot1, self.coarse_step, r - self.radius_offset)
            ring2 = self.circle_ring(rot2, self.coarse_step, r + self.radius_offset)
            d = self.dev_sum(ring1, ring2)
            if d < min_dev:
                min_dev, best = d, a
        rng = 2 * self.coarse_step
        min_dev_f, angle = float('inf'), best
        for a in np.arange(best - rng, best + rng, self.fine_step):
            rot1 = self.rotate(hsv1, -a)
            rot2 = self.rotate(hsv2, a)
            ring1 = self.circle_ring(rot1, self.fine_step, r - self.radius_offset)
            ring2 = self.circle_ring(rot2, self.fine_step, r + self.radius_offset)
            d = self.dev_sum(ring1, ring2)
            if d < min_dev_f:
                min_dev_f, angle = d, a
        return angle

    def blend(self, img1, img2, angle):
        inner = self.rotate(img1, -angle, interp=cv2.INTER_LINEAR, border=cv2.BORDER_CONSTANT)
        outer = self.rotate(img2, angle, interp=cv2.INTER_LINEAR, border=cv2.BORDER_CONSTANT)
        h1, w1 = inner.shape[:2]
        h2, w2 = outer.shape[:2]
        x0, y0 = (w2-w1)//2, (h2-h1)//2
        out = outer.copy()
        mask = (inner > 0).any(axis=2)
        out[y0:y0+h1, x0:x0+w1][mask] = inner[mask]
        _, buffer = cv2.imencode('.png', out)
        return base64.b64encode(buffer).decode('utf-8')

    def solve(self, path1, path2):
        img1 = cv2.imdecode(np.frombuffer(path1, np.uint8), cv2.IMREAD_COLOR)
        img2 = cv2.imdecode(np.frombuffer(path2, np.uint8), cv2.IMREAD_COLOR)
        angle = self.best_angle(img1, img2)
        out = self.blend(img1, img2, angle)
        return {'angle': round(angle, 2), 'base64': 'data:image/png;base64,' + out}