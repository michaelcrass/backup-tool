#import re
import os
import io
from datetime import date
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

def webpfiles():
    path = os.path.dirname(__file__)
    webp_files = []
    for root, dirs, files in os.walk(path):#"/directory_to_search"
        for file in files:
            if file.endswith(".webp"):
                webp_files.append(os.path.join(root, file))
    return webp_files


def logtxt(inhalt):
    dateiname =f"log_{date.today()}.txt"
    with io.open(dateiname,'a',encoding='utf8') as file:    
        file.write(inhalt + "\n") 
    print(inhalt)

def start():
    if not os.path.exists(zielpath):os.makedirs(zielpath)
    fehler=0
    for file_name in get_xfiles_in_folder("xlsx"):
        logtxt("***************************************************************")
        logtxt("Quelldatei: " + file_name)
        logtxt("Pfad: " + quellpath)
        source = quellpath + file_name
        destination = zielpath + file_name
        statinfo = os.stat(source)
        logtxt(f"Größe: {statinfo.st_size} Bytes")
        # copy only files
        if os.path.isfile(source):
            shutil.copy(source, destination)
            logtxt("Zieldatei: " + file_name)
            logtxt("Pfad: " + zielpath)
            statinfo2 = os.stat(destination)
            logtxt(f"Größe: {statinfo2.st_size} Bytes")
            if os.path.exists(destination):
                logtxt("erfolgreich: " + destination)
            if statinfo2.st_size != statinfo.st_size:
                fehler +=1
        logtxt("***************************************************************")
    logtxt(f"Fehler: {fehler}")
        

quellpath="D:\\"
zielpath =f"G:\\Meine Ablage\\Backups\\{date.today()}\\"
start()           