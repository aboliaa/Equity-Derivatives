# -*- mode: python -*-

from glob import glob

block_cipher = None


a = Analysis(['webserver\\main.py'],
             pathex=['.','C:\\DV\\src'],
             binaries=None,
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

t1 = Tree("templates", prefix="templates", excludes=["*.swp", ".DS_Store"])
t2 = Tree("static", prefix="static", excludes=["*.png", ".DS_Store", "*.swp"])
datas = t1 + t2

a.datas = datas

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Server',
          debug=False,
          strip=False,
          upx=True,
          console=True )
