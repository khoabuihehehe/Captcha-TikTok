import cv2
import base64
import numpy as np

class Puzzle:
    def trim(self, pc):
        pc = cv2.imdecode(np.frombuffer(pc, np.uint8), cv2.IMREAD_COLOR)
        h, w = pc.shape[:2]
        m_x, m_y, max_x, max_y = h, w, 0, 0
        for x in range(h):
            for y in range(w):
                if len(set(pc[x, y])) >= 2:
                    m_x, m_y = min(x, m_x), min(y, m_y)
                    max_x, max_y = max(x, max_x), max(y, max_y)
        return pc[m_x:max_x, m_y:max_y]

    def edges(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    def match(self, pc, bg, bg2):
        ph, pw = pc.shape[:2]
        res = cv2.matchTemplate(bg, pc, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)
        x, y = max_loc
        cv2.rectangle(bg2, (x, y), (x + pw, y + ph), (0, 0, 255), 2)
        _, buffer = cv2.imencode('.png', bg2)
        img = base64.b64encode(buffer).decode('utf-8')
        return {'angle': x, 'base64': "data:image/png;base64," + img}

    def solve(self, path1, path2):
        pc = self.trim(path1)
        bg = cv2.imdecode(np.frombuffer(path2, np.uint8), cv2.IMREAD_COLOR)
        return self.match(self.edges(pc), self.edges(bg), bg)