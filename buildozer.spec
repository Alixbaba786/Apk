[app]
title = pubg
package.name = pubg
package.domain = org.mygame
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Requirements mein android module zaroori hai
requirements = python3,kivy,android

# Screen orientation aur full screen settings
orientation = sensor
fullscreen = 1

# Internet permission ke bina blank white screen ayegi
android.permissions = INTERNET

# Modern phones ke liye architectures
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
