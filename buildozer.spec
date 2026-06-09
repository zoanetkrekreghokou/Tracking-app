[app]

title = Tracking app
package.name = Trackingapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requirements ordered for proper compilation
requirements = python3,kivy,opencv,numpy,pyjnius

orientation = portrait

# Modern Android permissions
android.permissions = CAMERA, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW

# API settings mandatory for numpy and modern devices
android.api = 34
android.minapi = 24
android.ndk = 26b

# Environment variable needed for building numpy
android.ext_build_env = P4A_NUMPY_BUILD=1

# Architecture optimization for 64-bit devices
android.archs = arm64-v8a

android.logcat_filters = *:S python:D
android.accept_sdk_license = True

[buildozer]
log_level = 2
