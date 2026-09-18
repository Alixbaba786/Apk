[app]

# (str) Title of your application
title = Royal 3D Chess

# (str) Package name
package.name = royalchess

# (str) Package domain (needed for android/ios packaging)
package.domain = com.royal.chess

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.3.0,python-chess

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, POST_NOTIFICATIONS

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version (Deprecated: Commented out to prevent warnings)
# android.sdk = 33

# (str) Android NDK version (Fixed: Changed to valid release string to prevent HTTP 404 Error)
android.ndk = 25b

# (bool) Auto-accept Android SDK licenses
android.accept_sdk_license = True

# (bool) Use --private data dir (True), or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a lib dir and copy only .so
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

