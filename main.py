from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

# Code Android safe : marche aussi sur PC
ANDROID = False
try:
    from android.permissions import request_permissions, Permission
    from android import activity
    ANDROID = True
except ImportError:
    pass

def ask_permissions(dt):
    if ANDROID:
        request_permissions([Permission.SYSTEM_ALERT_WINDOW, Permission.INTERNET])
        # Si pas encore autorisé, ouvre les paramètres
        if not activity.check_permission("android.permission.SYSTEM_ALERT_WINDOW"):
            activity.start_activity("android.settings.action.MANAGE_OVERLAY_PERMISSION")

class TrackingApp(App):
    def build(self):
        # Attend 1s avant de demander les perms pour éviter le crash au démarrage
        Clock.schedule_once(ask_permissions, 1)
        return Label(text="Tracking App\nActive l'overlay dans les paramètres si demandé")

if __name__ == "__main__":
    TrackingApp().run()
