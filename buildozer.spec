[app]

# (str) Title of your application
title = Royal 3D Chess

# (str) Package name
package.name = royalchess

# (str) Package domain (needed for android packaging)
package.domain = com.royal.chess

# (str) Source code where main.py resides
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,python-chess==1.999

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, POST_NOTIFICATIONS

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (int) Android SDK version
android.sdk = 33

# (str) Android NDK version
android.ndk = 25.2.9519653

# (bool) Accept Android SDK licenses
android.accept_sdk_license = True

# (bool) Private data dir storage
android.private_storage = True

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copy library
android.copy_libs = 1

# (str) Android architecture targets
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if run as root
warn_on_root = 1
