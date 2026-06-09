[app]

# (Idem) Nom de l'application affiché sur le téléphone
title = Tracking app

# (Idem) Identifiant unique du paquet
package.name = Trackingapp
package.domain = org.test

# (Idem) Emplacement du code source
source.dir = .

# Extensions de fichiers à inclure dans l'APK
source.include_exts = py,png,jpg,kv,atlas

# (Idem) Version de l'application
version = 0.1

# CORRECTION CRITIQUE : Utilisation de la recette native 'opencv' à la place du paquet pip de bureau
requirements = python3,kivy,opencv,numpy,pyjnius

# (Idem) Force l'affichage en mode Portrait
orientation = portrait

# CORRECTION CRITIQUE : Nettoyage et mise à niveau des permissions pour Android 11 à 14+
# Ajout de MANAGE_EXTERNAL_STORAGE pour remplacer les anciennes permissions de stockage si vous ciblez l'API 31+
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW

# MISE À NIVEAU : L'API 33 ou 34 est fortement recommandée pour la compatibilité avec le Play Store actuel et le NDK 28c de votre workflow
android.api = 34
android.minapi = 21

# OPTIMISATION CI : Compilation multi-architecture indispensable pour les téléphones modernes (64-bit et 32-bit)
android.archs = arm64-v8a, armeabi-v7a

# (Idem) Filtres de logs utiles pour déboguer votre application avec adb logcat
android.logcat_filters = *:S python:D

# OPTIMISATION : Indique à Buildozer d'accepter automatiquement les licences d'API supérieures (34)
android.accept_sdk_license = True

[buildozer]
# (Idem) Niveau de log maximum pour voir le détail des erreurs dans GitHub Actions
log_level = 2
