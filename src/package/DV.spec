# -*- mode: python -*-

block_cipher = None

m_a = Analysis(['webserver\\main.py'],
             pathex=['.', 'C:\\DV\\src'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

p_a = Analysis(['data\\populate_csvs.py'],
             pathex=['.', 'C:\\DV\\src'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

MERGE( (m_a, 'Server', 'Server.exe'), (p_a, 'DBUpdater', 'DBUpdater.exe') )

m_pyz = PYZ(m_a.pure, m_a.zipped_data,
             cipher=block_cipher)
m_exe = EXE(m_pyz,
          m_a.scripts,
          exclude_binaries=True,
          name='Server',
          debug=False,
          strip=False,
          upx=True,
          console=True )

p_pyz = PYZ(p_a.pure, p_a.zipped_data,
             cipher=block_cipher)

p_exe = EXE(p_pyz,
          p_a.scripts,
          exclude_binaries=True,
          name='DBUpdater',
          debug=False,
          strip=False,
          upx=True,
          console=True )

m_coll = COLLECT(m_exe,
               m_a.binaries,
               m_a.zipfiles,
               m_a.datas,
			   Tree("templates", prefix="templates", excludes=["*.swp", ".DS_Store"]),
			   Tree("static", prefix="static", excludes=["*.png", ".DS_Store", "*.swp"]),
               strip=False,
               upx=True,
               name='Server')

p_coll = COLLECT(p_exe,
               p_a.binaries,
               p_a.zipfiles,
               p_a.datas,
               strip=False,
               upx=True,
               name='DBUpdater')

