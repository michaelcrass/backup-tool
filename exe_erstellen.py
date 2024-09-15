import PyInstaller.__main__

PyInstaller.__main__.run([
    'backup_tool.py',
    '--onefile',
    # '--onedir',
    # '-w'   #als demon = ohne shell
])