# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

hiddenimports = [
    "i18n",
    "customtkinter",
    "tkinter",
    "tkinter.scrolledtext",
    "tkinter.messagebox",
    "tkinter.ttk",
]

excludes = [
    "numpy",
    "pandas",
    "scipy",
    "PIL",
    "Pillow",
    "cv2",
    "matplotlib",
    "pytest",
    "unittest",
    "pydoc",
    "doctest",
    "difflib",
    "xmlrpc",
    "xmlrpc.client",
    "xmlrpc.server",
    "http.server",
    "wsgiref",
    "multiprocessing",
    "concurrent.futures",
    "asyncio",
    "sqlite3",
    "dbm",
    "distutils",
    "setuptools",
    "pkg_resources",
    "pip",
    "IPython",
    "jupyter",
    "lib2to3",
    "ensurepip",
    "turtledemo",
    "tkinter.test",
]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[("assets", "assets")],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    cipher=block_cipher,
    noarchive=False,
    optimize=2,
)

def _keep_binary(item):
    dest = item[0].replace("\\", "/").lower()
    skip = (
        "/tk/demos/",
        "/tcl/tzdata/",
        "/tcl/opt0.4/",
        "/tk/images/logo",
        "/tk/images/README",
    )
    return not any(token in dest for token in skip)

a.binaries = [item for item in a.binaries if _keep_binary(item)]
a.datas = [item for item in a.datas if _keep_binary(item)]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="fishtest-worker-gui",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/icon.ico",
)
