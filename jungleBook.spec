# -*- mode: python -*-
a = Analysis(['jungleBook.py'],
             pathex=['D:\\Dropbox\\code\\projects\\tarzan'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='jungleBook.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='icon.ico')
