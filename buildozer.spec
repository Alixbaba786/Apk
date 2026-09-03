[app]
title = Royal Casino USDT
package.name = royalcasinousdt
package.domain = org.royalcasino
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Corrected dependencies for Kivy + SSL/HTTPS Support
requirements = python3,kivy==2.3.0,openssl,certifi

orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.accept_sdk_license = True

# Standard Stable NDK & API Config
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
