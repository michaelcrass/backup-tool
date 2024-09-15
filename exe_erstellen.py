import PyInstaller.__main__

PyInstaller.__main__.run([
    'backup_tool.py',
    '--onefile',
    '-w'   #als demon = ohne shell
])