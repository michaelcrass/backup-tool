#import re
import os
import io
from datetime import date
from datetime import datetime
import shutil


def get_files_in_folder():
    dir_path = os.path.dirname(__file__)
    dir_path = os.path.dirname(quellpath)
    res = []
    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)):
            res.append(file_path)
    return res
    
def get_xfiles_in_folder(dateiendung):
    y = []
    for x in get_files_in_folder():
        if x[-5:]==f".{dateiendung}":
            y.append(x)
    return y

def logtxt(inhalt):
    dateiname =f"{zielpath}log_{date.today()}.txt"
    with io.open(dateiname,'a',encoding='utf8') as file:    
        file.write(inhalt + "\n") 
    print(inhalt)

def start():
    if not os.path.exists(zielpath):os.makedirs(zielpath)
    fehler=0
    for file_name in get_xfiles_in_folder("xlsx"):
        logtxt("***************************************************************")
        logtxt(f"{datetime.now()}")
        logtxt("Quelldatei: " + file_name)
        logtxt("\tPfad: " + quellpath)
        source = quellpath + file_name
        destination = zielpath + file_name
        statinfo = os.stat(source)
        logtxt(f"\tGröße: {statinfo.st_size} Bytes")
        # copy only files
        if file_name[0] == "~":
            logtxt("\ttemporäre Datei übersprungen")
            continue
        if os.path.isfile(source):
            shutil.copy(source, destination)
            logtxt("Zieldatei: " + file_name)
            logtxt("\tPfad: " + zielpath)
            statinfo2 = os.stat(destination)
            logtxt(f"\tGröße: {statinfo2.st_size} Bytes")
            if os.path.exists(destination):
                if statinfo2.st_size == statinfo.st_size:
                    logtxt("\terfolgreich: " + destination)
                else:
                    fehler +=1
                    logtxt("\tFehler beim Kopieren: " + destination)
                    logtxt("\tFehler: Dateigröße stimmt nicht")
            else:
                logtxt("\tFehler: Kopieren fehlgeschlagen")
                fehler +=1
        logtxt("***************************************************************")
    print(f"Fehler: {fehler}")
    if fehler==0:
        print("ok")
    else:
        input("")
        

quellpath="D:\\"
zielpath =f"G:\\Meine Ablage\\Backups\\{date.today()}\\"
start()           