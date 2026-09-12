[app]
title = PK786 Casino
package.name = pk786casino
package.domain = com.pk786.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Essential libraries for Python & Supabase/Telegram REST APIs
requirements = python3,kivy,openssl,urllib3,certifi,hostpython3

orientation = portrait
fullscreen = 0
android.presplash_color = #070910

# Network permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Target API configuration for modern Android
android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Acceptance of SDK/NDK licenses
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

