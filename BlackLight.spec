# -*- mode: python -*-
a = Analysis(['BlackLight.py'],
             pathex=['D:\\Dropbox\\code\\projects\\blacklight'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='BlackLight.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='icon_small.ico')

a.datas += [('icons/open.png', 'D:/Dropbox/code/projects/blacklight/icons/open.png',  'DATA')]   