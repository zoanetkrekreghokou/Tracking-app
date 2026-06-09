from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import cv2
import numpy as np

# Utilisation du tracker CSRT (plus précis) ou KCF (plus rapide)
TRACKER_TYPE = 'CSRT'  # ou 'KCF'

class ObjectTracker:
    def __init__(self):
        self.cap = None
        self.tracker = None
        self.tracking = False
        self.frame = None
        self.bbox = None

    def init_camera(self, cam_id=0):
        self.cap = cv2.VideoCapture(cam_id)
        # Réduire la résolution pour la performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def select_roi(self, frame):
        """Permet à l'utilisateur de sélectionner une zone (à faire dans l'app Kivy via un canvas)"""
        # Ici on simule : on prend la moitié centrale comme zone par défaut
        h, w = frame.shape[:2]
        self.bbox = (w//4, h//4, w//2, h//2)
        return self.bbox

    def init_tracker(self, frame, bbox):
        if TRACKER_TYPE == 'CSRT':
            self.tracker = cv2.TrackerCSRT_create()
        else:
            self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(frame, bbox)
        self.tracking = True

    def update(self, frame):
        if not self.tracking or self.tracker is None:
            return frame
        success, self.bbox = self.tracker.update(frame)
        if success:
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), 2)
            # Optionnel : centre
            cx = int(self.bbox[0] + self.bbox[2]/2)
            cy = int(self.bbox[1] + self.bbox[3]/2)
            cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
        else:
            cv2.putText(frame, "Objet perdu", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),2)
        return frame

class TrackerCamApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.image = Image()
        self.btn_select = Button(text="Sélectionner objet (ROI)", size_hint=(1, 0.1))
        self.btn_select.bind(on_press=self.start_selection)
        layout.add_widget(self.image)
        layout.add_widget(self.btn_select)
        self.tracker = ObjectTracker()
        self.tracker.init_camera()
        Clock.schedule_interval(self.update, 1/30)  # 30 fps
        return layout

    def start_selection(self, instance):
        # À compléter : utiliser un widget de dessin pour sélectionner
        # Pour simplifier, on prend une zone fixe
        ret, frame = self.tracker.cap.read()
        if ret:
            h, w = frame.shape[:2]
            bbox = (w//3, h//3, w//3, h//3)
            self.tracker.init_tracker(frame, bbox)

    def update(self, dt):
        ret, frame = self.tracker.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)  # effet miroir
        frame = self.tracker.update(frame)
        # Convertir pour Kivy
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def on_stop(self):
        if self.tracker.cap:
            self.tracker.cap.release()

if __name__ == '__main__':
    TrackerCamApp().run()
