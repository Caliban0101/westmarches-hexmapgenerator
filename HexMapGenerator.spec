# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['hex_map_generator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add customtkinter assets
import customtkinter
import os

ctk_path = os.path.dirname(customtkinter.__file__)
a.datas += [(os.path.join('customtkinter', os.path.relpath(root, ctk_path), file), 
             os.path.join(root, file), 
             'DATA') 
            for root, dirs, files in os.walk(ctk_path) 
            for file in files]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HexMapGenerator-CTK',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
