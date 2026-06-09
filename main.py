from kivy.app import App
from kivy.uix.label import Label

# Import pour Android
try:
    from android.permissions import request_permissions, Permission
    ANDROID = True
except:
    ANDROID = False

class TrackingApp(App):
    def build(self):
        # Demande les permissions au démarrage sur Android
        if ANDROID:
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        
        return Label(text="App lancée !")

if __name__ == "__main__":
    TrackingApp().run()
