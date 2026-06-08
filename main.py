from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import time

# Plages HSV calibrées pour tes gobelets King Thimbles
LOWER_CUP = np.array([8, 70, 40])
UPPER_CUP = np.array([25, 255, 180])
LOWER_CROWN = np.array([20, 100, 200])
UPPER_CROWN = np.array([35, 255, 255])

class KingThimblesTracker:
    def __init__(self):
        self.cible = None
        self.last_seen = time.time()
        self.dx, self.dy = 0, 0
        self.pos_history = []

    def capture_screen_android(self):
        # Capture d’écran Android via pyjnius
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        view = activity.getWindow().getDecorView().getRootView()

        from android.graphics import Bitmap, Canvas
        bitmap = Bitmap.createBitmap(view.getWidth(), view.getHeight(),
                                     Bitmap.Config.ARGB_8888)
        canvas = Canvas(bitmap)
        view.draw(canvas)

        # Convertit Bitmap -> numpy array BGR
        buffer = bitmap.getPixels()
        frame = np.array(buffer, dtype=np.uint8).reshape(view.getHeight(), view.getWidth(), 4)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        return frame

    def detecter_gobelets(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_cup = cv2.inRange(hsv, LOWER_CUP, UPPER_CUP)
        mask_crown = cv2.inRange(hsv, LOWER_CROWN, UPPER_CROWN)
        mask = cv2.bitwise_or(mask_cup, mask_crown)

        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objets = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 800 < area < 15000:
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w//2, y + h//2
                objets.append({'x': cx, 'y': cy, 'w': w, 'h': h})
        return objets

    def update(self, frame):
        objets = self.detecter_gobelets(frame)

        if len(self.pos_history) >= 2:
            self.dx = self.pos_history[-1][0] - self.pos_history[-2][0]
            self.dy = self.pos_history[-1][1] - self.pos_history[-2][1]

        pred_x, pred_y = 0, 0
        if self.cible:
            pred_x = self.cible['x'] + self.dx
            pred_y = self.cible['y'] + self.dy
            cv2.circle(frame, (int(pred_x), int(pred_y)), 8, (0,255,255), -1)

        if objets:
            if self.cible:
                meilleur = min(objets, key=lambda o: ((o['x']-pred_x)**2 + (o['y']-pred_y)**2)**0.5)
                distance = ((meilleur['x']-pred_x)**2 + (meilleur['y']-pred_y)**2)**0.5
                score = max(0, 100 - distance/2)
                if score > 60:
                    self.cible = meilleur
                    self.last_seen = time.time()
            else:
                self.cible = objets[0]
                self.last_seen = time.time()

        if self.cible:
            cv2.rectangle(frame,
                         (self.cible['x']-self.cible['w']//2, self.cible['y']-self.cible['h']//2),
                         (self.cible['x']+self.cible['w']//2, self.cible['y']+self.cible['h']//2),
                         (0,255,0), 3)
            self.pos_history.append((self.cible['x'], self.cible['y']))
            if len(self.pos_history) > 5:
                self.pos_history.pop(0)
        elif time.time() - self.last_seen > 1:
            self.cible = None
            self.pos_history = []

        return frame

class TrackerApp(App):
    def build(self):
        self.img = Image()
        self.tracker = KingThimblesTracker()
        Clock.schedule_interval(self.update, 1/30)
        return self.img

    def update(self, dt):
        frame = self.tracker.capture_screen_android()
        frame = self.tracker.update(frame)

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture

if __name__ == '__main__':
    TrackerApp().run()
