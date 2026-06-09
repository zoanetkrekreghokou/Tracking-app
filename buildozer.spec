[app]

# Nom de l'application affiché sur le téléphone
title = Tracking app

# Identifiant unique du paquet
package.name = Trackingapp
package.domain = org.test

# Emplacement du code source
source.dir = .

# Extensions de fichiers à inclure dans l'APK
source.include_exts = py,png,jpg,kv,atlas

# Version de l'application
version = 0.1

# Recettes de compilation natives requises (l'ordre est important)
requirements = python3,kivy,opencv,numpy,pyjnius

# Force l'affichage en mode Portrait
orientation = portrait

# Nettoyage et mise à niveau des permissions pour Android 11 à 14+
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW

# Niveau de l'API Android cible et minimum requis
android.api = 34
android.minapi = 21

# Version du NDK stable fortement recommandée pour OpenCV / NumPy
android.ndk = 26b

# Variable d'environnement CRITIQUE pour forcer la compilation propre de NumPy
android.ext_build_env = P4A_NUMPY_BUILD=1

# Compilation ciblée sur l'architecture moderne des smartphones (64-bit)
android.archs = arm64-v8a

# Filtres de logs utiles pour déboguer votre application avec adb logcat
android.logcat_filters = *:S python:D

# Indique à Buildozer d'accepter automatiquement les licences d'API supérieures
android.accept_sdk_license = True

[buildozer]
# Niveau de log maximum pour voir le détail des erreurs dans GitHub Actions
log_level = 2
