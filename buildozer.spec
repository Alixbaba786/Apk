[app]
title = PK786 Casino
package.name = pk786casino
package.domain = com.pk786.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

requirements = python3,kivy,openssl,urllib3,certifi

orientation = portrait
osx.kivy_version = 2.3.0
fullscreen = 0
android.presplash_color = #070910

# Permissions needed for REST API & Telegram alerts
android.permissions = INTERNET, ACCESS_NETWORK_STATE

android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
