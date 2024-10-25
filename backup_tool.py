import logging
import os
import datetime
import shutil
import configparser
import logging
from datetime import date,datetime 
import pathlib
import sys
import zipfile

class Programm:
    def __init__(self):
        # read config
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
        except ValueError as e:
            print(f"Fehler: {e}")
            input("..")

        # Configure logging
        self._logger = logging.getLogger(__name__)
        logging_format = config.get('logging', 'logging_format', raw=True)
        logging.basicConfig(filename=config['logging']['log_file'], level=config['logging']['logging_level'],format=logging_format)

        #logging
        pythonversion = "{0}.{1}.{2}".format(sys.version_info.major,sys.version_info.minor,sys.version_info.micro)
        self._logger.info(f"Python-Version: {pythonversion}")
        self._logger.info(f"Python-Script: {__file__}]")
        self._logger.info(f"User: {os.getenv('USERNAME')}@{os.getenv('COMPUTERNAME')}")

        # paths
        self.source_path=config['backup']['source_path']
        self.target_path =config['backup']['target_path']
        self.zip_only =config['backup']['zip_only']
        self.target_pathparent =config['backup']['target_path']
        self.target_path =f"{self.target_pathparent}{date.today()}\\"
        
        # self.save_filetype =config['backup']['save_filetype']
        self._logger.info("read list of file typs to save")
        self.save_filetype_list = []
        items = config['backup']['save_filetype'].split(sep=",")
        for x in items:
            self.save_filetype_list.append(x)
            self._logger.info(f"Dateityp: {x}")      

        self.zipname = f"backup_{date.today()}.zip" 

        self.fehler=0
        self.fehlertext=""
        self.filelist = []

        self.start()
        
    def get_subfolders(self,directory):
        # Get all subfolders in the given directory
        return [f.path for f in os.scandir(directory) if f.is_dir()]

    def get_folder_date(self,folder_name):
        # Extract the date from the folder name in the format YYYY-MM-DD
        try:
            return datetime.strptime(folder_name, '%Y-%m-%d')
        except ValueError as e:
            self.fehler += 1
            self._logger.warning(f"Fehler: {e}")
            return None

    def filter_folders_to_keep(self,subfolders):
        # Sort folders by date (assuming date is part of the folder name)
        dated_folders = [(folder, self.get_folder_date(os.path.basename(folder))) for folder in subfolders]
        dated_folders = [f for f in dated_folders if f[1] is not None]
        dated_folders.sort(key=lambda x: x[1], reverse=True)

        # Keep the five latest folders
        folders_to_keep = [f[0] for f in dated_folders[:5]]
        return folders_to_keep

    def get_folder_size(self,folder):
        # Calculate the size of a folder in bytes
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def delete_folders(self,subfolders, folders_to_keep):
        total_deleted_size = 0
        # Delete the folders that are not in the folders_to_keep list
        for folder in subfolders:
            if folder not in folders_to_keep:
                folder_size = self.get_folder_size(folder)
                total_deleted_size += folder_size
                self._logger.warning(f"Deleting folder: {folder}")
                shutil.rmtree(folder)
        return total_deleted_size


    def get_files_in_folder(self):
        dir_path = os.path.dirname(__file__)
        dir_path = os.path.dirname(self.source_path)
        res = []
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                res.append(file_path)
        return res

    def get_xfiles_in_folder(self):
        y = []
        for x in self.get_files_in_folder():
            # Dateiendung, aber ohne Punkt
            # if pathlib.Path(x).suffix[1:] == f".{dateiendung}":
            if x[0] == "~":
                self._logger.info("Temporary file skipped")
                continue
            if pathlib.Path(x).suffix[1:] in self.save_filetype_list:
                y.append(x)           
        return y
    
    def create_zip(self,files, zip_name, compress=True):
        """Create a zip file with options to compress and encrypt."""
    
        compression = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED

        with zipfile.ZipFile(os.path.join(self.source_path,zip_name), 'w', compression=compression) as zipf:
        # with zipfile.ZipFile(zip_name, 'w', compression=compression) as zipf:
            for file in files:
                zipf.write(os.path.join(self.source_path, file), os.path.basename(file))
                # zipf.write(file, os.path.basename(file))

        self._logger.info(f'ZIP file created: {zip_name}')    
    

    def delete_file_if_exists(self,filepath):
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self._logger.info(f"File '{filepath}' has been deleted.")
            else:
                self._logger.info(f"File '{filepath}' does not exist.")
        except Exception as e:
            self._logger.warning(f"An error occurred: {e}")

    def start(self):
        self._logger.info(f"source_path: {self.source_path}")
        self._logger.info(f"target_path: {self.target_path}")

        if not os.path.exists(self.target_path):os.makedirs(self.target_path)


        

        if self.zip_only.lower() == "true":
            self.create_zip(self.get_xfiles_in_folder(),self.zipname)
            self.filelist = [self.zipname]
        else:
            self.filelist = self.get_xfiles_in_folder()

        
        for file_name in self.filelist:
            self._logger.info("Zu sichernde Datei: " + file_name)
        
            source = self.source_path + file_name
            destination = self.target_path + file_name
            statinfo = os.stat(source)

            # copy only files
            if file_name[0] == "~":
                self._logger.info("Temporary file skipped")
                continue
            if os.path.isfile(source):
                shutil.copy(source, destination)
                self._logger.info("Source: " + source)
                self._logger.info("Destination: " + destination)
                statinfo2 = os.stat(destination)
                self._logger.info(f"Size: {statinfo2.st_size} Bytes")
                if os.path.exists(destination):
                    if statinfo2.st_size == statinfo.st_size:
                        self._logger.info("erfolgreich: " + destination)
                    else:
                        self.fehler +=1
                        self._logger.error("Fehler beim Kopieren: " + destination)
                        self._logger.error("Dateigröße stimmt nicht")
                        self.fehlertext += "Kopieren fehlgeschlagen. Dateigröße stimmt nicht: " + destination + "\n"
                else:
                    self._logger.error("Kopieren fehlgeschlagen")
                    self.fehler +=1
                    self.fehlertext += "Kopieren fehlgeschlagen: " + destination + "\n"

        subfolders = self.get_subfolders(self.target_pathparent)
        self._logger.info(f"Subfolders: {subfolders}")
        folders_to_keep = self.filter_folders_to_keep(subfolders)
        self._logger.info(f"Folders to keep: {folders_to_keep}")
        total_deleted_size = self.delete_folders(subfolders, folders_to_keep)
        self._logger.info(f"Total size of deleted folders: {total_deleted_size / (1024 * 1024):.2f} MB")

        self.delete_file_if_exists(os.path.join(self.source_path,self.zipname))
        
        self._logger.info(f"Fehler: {self.fehler}")
        
        if self.fehler==0:
            print("ok")
        else:
            print(f"Fehler: {self.fehler}")
            input("")


if __name__ == '__main__':
    Programm()