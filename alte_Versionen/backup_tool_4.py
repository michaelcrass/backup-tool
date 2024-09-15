#import re
import os
import io
from datetime import date
from datetime import datetime
import shutil
#from time import sleep


def get_subfolders(directory):
    # Get all subfolders in the given directory
    return [f.path for f in os.scandir(directory) if f.is_dir()]

def get_folder_date(folder_name):
    # Extract the date from the folder name in the format YYYY-MM-DD
    try:
        return datetime.strptime(folder_name, '%Y-%m-%d')
    except ValueError as e:
        print(f"Fehler: {e}")
        return None

def filter_folders_to_keep(subfolders):
    # Sort folders by date (assuming date is part of the folder name)
    dated_folders = [(folder, get_folder_date(os.path.basename(folder))) for folder in subfolders]
    dated_folders = [f for f in dated_folders if f[1] is not None]
    dated_folders.sort(key=lambda x: x[1], reverse=True)

    # Keep the five latest folders
    folders_to_keep = [f[0] for f in dated_folders[:5]]
    return folders_to_keep

def get_folder_size(folder):
    # Calculate the size of a folder in bytes
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def delete_folders(subfolders, folders_to_keep):
    total_deleted_size = 0
    # Delete the folders that are not in the folders_to_keep list
    for folder in subfolders:
        if folder not in folders_to_keep:
            folder_size = get_folder_size(folder)
            total_deleted_size += folder_size
            print(f"Deleting folder: {folder}")
            shutil.rmtree(folder)
    return total_deleted_size


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
    
    logtxt("***************************************************************")
    logtxt("***************************************************************")
    # delete folders, keep the five latest backup folders
    # 2024-03-24

    #sleep(2)
    subfolders = get_subfolders(gdrive_path)
    folders_to_keep = filter_folders_to_keep(subfolders)
    logtxt(f"Folders to keep: {folders_to_keep}")
    total_deleted_size = delete_folders(subfolders, folders_to_keep)
    logtxt(f"Total size of deleted folders: {total_deleted_size / (1024 * 1024):.2f} MB")
    
    logtxt("***************************************************************")
    logtxt("***************************************************************")
    print(f"Fehler: {fehler}")
    if fehler==0:
        print("ok")
    else:
        input("")
        

quellpath="D:\\"
gdrive_path =f"G:\\Meine Ablage\\Backups\\"
zielpath =f"{gdrive_path}{date.today()}\\"
start()           