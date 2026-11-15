
[app]

title = JARVIS 3.0
package.name = jarvisapp
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 3.0

requirements = python3,kivy,requests,plyer,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,MODIFY_AUDIO_SETTINGS

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
