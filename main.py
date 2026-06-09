from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# Import Android permissions - nouvelle syntaxe qui remplace android.activity.check_permission
try:
    from android.permissions import request_permissions, Permission
    ANDROID = True
except ImportError:
    ANDROID = False

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Tracking App - Prête'))
        self.add_widget(Label(text='Permissions demandées au démarrage'))

class TrackingApp(App):
    def build(self):
        # Demande les permissions Android au lancement
        if ANDROID:
            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.SYSTEM_ALERT_WINDOW
            ])
        
        return MainWidget()

if __name__ == '__main__':
    TrackingApp().run()
