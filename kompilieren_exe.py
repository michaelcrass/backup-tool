import PyInstaller.__main__

# requirements:
# pip install -r requirements.txt
# py -m pip install pigar
# # py -m pigar generate


PyInstaller.__main__.run([
    'backup_tool.py',
    '--onefile',
    '--icon=safe.ico',
    # '--onedir',
    # '-w'   #als demon = ohne shell
])