[app]
title = KingTracker
package.name = kingtracker
package.domain = org.test
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = kivy,opencv-python-headless,numpy,pyjnius
orientation = portrait
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW
android.api = 31
android.minapi = 21
android.arch = arm64-v8a
android.logcat_filters = *:S python:D
[buildozer]
log_level = 2
