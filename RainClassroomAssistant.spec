# -*- mode: python ; coding: utf-8 -*-

import os
import apprise

apprise_path = os.path.dirname(apprise.__file__)


a = Analysis(
    ['RainClassroomAssistant.py'],
    pathex=[],
    binaries=[],
    datas=[('UI/Image/favicon.ico','UI/Image'),('UI/Image/NoRainClassroom.jpg','UI/Image'), (apprise_path, 'apprise')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    collect_all=['apprise'],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RainClassroomAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['UI\\Image\\favicon.ico'],
    version='file_version_info.txt'
)

app = BUNDLE(exe,
    name='RainClassroomAssistant.app',
    icon=None,
    bundle_identifier=None,
    version='0.5.2',
)