from typing import Union, List, Tuple, Iterator, Optional, Dict

import pendulum
import shutil
import sys

from pathlib import Path
from time import ctime

from RemoveMedia.configuration.read_config import Reader
from RemoveMedia.configuration import generate_config as gc
from RemoveMedia.configuration.log import Log
from RemoveMedia.notification import plex, pbullet

class Base:
    
    def __init__(self,
        threshold : Optional[int] = None,
        folder : Optional[Union[List[str], str]] = None,
        threshold_type : Optional[str] = None,
        log_path : Optional[str] = None,  
        log_filename : Optional[str] = None,
        plex : Optional[str] = None,
        pb_api_key : Optional[str] = None,        
        config : Optional[str] = None
        ) -> None:
        """Class to stock and remove folder in a given folder
        
        treshold : int
            number to keep a file on the server
        folder : str
            path to folder you want to look for file to removed
        treshold_type : str
            specify type of treshold [years, months, weeks, days, hours, seconds, remaining_days, remaining_seconds]
        log_path : str 
            path to store log file
        log_filename : str
            name of file to save log
        plex : str
            full url to refresh plex http://[PMS_IP_Address]:32400/library/sections/all/refresh?X-Plex-Token=[token]
        pb_api_key : str
            pushbullet API key
        config : str
            config filename to use
        
        Returns
        -------
        None
        """
        #conf file 
        read = Reader(config)
        
        #attribute
        self.threshold = read.select_value(threshold, "folder", "threshold", method = "getint")
        self.path = read.select_value(folder, "folder",  "path")
        if "," in self.path:
            strip = lambda x: x.strip()
            self.path = list(map(strip, self.path.split(",")))
        self.threshold_type = read.select_value(threshold_type, "folder", "threshold_type")
        self.plex = read.select_value(plex, "plex", "link", fallbac = None)
        self.pb_api_key = read.select_value(pb_api_key, "pushbullet", "api_key", fallbac = None)
        #Log
        journal = Log(log_path=log_path, log_filename=log_filename, config=config)
        self.log = journal.log
        self.today = gc.Now
        self.log.info(f" {self.__class__.__name__} Initialization done", extra={"folder" : self.path})
       
      
    def _yield_folder_info(self
        ) -> Iterator[Tuple[str, Path]]:
            """
            foreach folder supply as string or in list, this function will yield name, and path.
            Parameters
            ------------------
            folder : List[str], str
                string of path to a given folder, multiple folder can be supply as string
             Yields
             ----------
             name : str
                 foldet name only
              path : Path
                  path to folder as Path
            """
            if isinstance(self.path, list):
                for dossier in self.path:             
                    yield self._get_name_path(dossier)
            else:
                 yield self._get_name_path(self.path)
    
    def _get_name_path(self,
        folder :  Union[List[str], str]
        ) -> Tuple[str, Path]:
            """
            folder supply as string will  be return  as name and path.
            Parameters
            ------------------
            folder : List[str], str
                string of path to a given folder, multiple folder can be supply as string
             Returns
             ----------
             name : str
                 foldet name only
              path : Path
                  path to folder as Path
            """
            path = Path(folder).resolve()
            self._folder_exist(path)
            name = path.name
            return name, path        
                    
    def _folder_exist(self,
        folder_path : Path
        ) -> None:
        """
        test if folder exist or not
        Parameters:
         -------------------
         folder_path : Path
             path to a given folder
         Returns
         -------------
         folder_exist : bool
             True if folder exist else exists systeme.raise FileNotFoundError
        """
        if folder_path.exists():
            self.log.info(f"{folder_path} exist", extra={"folder" : folder_path.name})
            return True
        else:
            self.log.info(f"{folder_path} do not exist", extra={"folder" : folder_path.name})
    
    def _notify(self, 
        name : str, 
        n_remove : int,
        list_remove : List[str]
        ) -> None:
        """
        toogle method to notify plex or pushbullet
        Parameters
        --------------------
        name : str
            parent folder name from woch file and folder a re remove
        n_remove : int
            Count of files/folders removed
        list_remove : List[str]
            Name list of removed files/folder
        Return
        -----------
        None           
        """
        if self.plex:
            plex.plex(self.plex, self.log, name)
        if self.pb_api_key : 
            pbullet.pbullet(self.pb_api_key, name, n_remove, list_remove, self.log)
            