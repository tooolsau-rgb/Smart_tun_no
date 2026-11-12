[app]
title = SmartClaw
package.name = smartclaw
package.domain = com.smartclaw.client
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0.0
requirements = python3,kivy,requests,certifi,urllib3,charset_normalizer,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 35
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
p4a.bootstrap = sdl2
[buildozer]
log_level = 2
warn_on_root = 1
