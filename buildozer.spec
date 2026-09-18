[app]
# (str) Title of your application
title = My Application

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Yahan Kivy ka version 2.2.1 fix kiya hai taaki Cython 0.29.33 ke saath perfect match ho
requirements = python3,kivy==2.2.1

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# --- Android specific ---

# (list) Permissions
# android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# Sirf arm64-v8a aur armeabi-v7a rakha hai taaki build fast ho aur sabhi modern phones par chale
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backups (Android 6.0+)
android.allow_backup = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1


