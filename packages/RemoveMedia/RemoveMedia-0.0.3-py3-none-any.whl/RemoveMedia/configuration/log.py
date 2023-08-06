from typing import Union, List, Tuple, Iterator, Optional, Dict

import pendulum
import logging
import shutil
import urllib.request
import sys

from pathlib import Path
from time import ctime
from RemoveMedia.configuration.read_config import Reader

class Log:
    
    def __init__(self,
        log_path : Optional[str] = None,  
        log_filename : Optional[str] = None,        
        config : Optional[str] = None
        ) -> None:
        """Class to stock and remove folder in a given folder
        
        log_path : str 
            path to store log file
        log_filename : str
            name of file to save log
        config : str
            config filename to use
        
        Returns
        -------
        None
        """
        #read config file
        read = Reader(config)
        self.configuration = read.configuration
        #attribute
        self.log_path = read.select_value(log_path, "log", "log_path", fallbac = Path(Path(__file__).parent.parent / "log"))
        self.log_filename = read.select_value(log_filename, "log", "log_filename", fallbac = "removedMedia.log")

    @property                                                                    
    def log(self):
        # Create the Logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
     
        # Create the Handler for logging data to a file
        log_handler = logging.FileHandler(self._log_full_path())
        log_handler.setLevel(logging.DEBUG)
     
        # Create a Formatter for formatting the log messages
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - Folder : %(folder)s - %(message)s')
     
        # Add the Formatter to the Handler
        log_handler.setFormatter(log_formatter)
     
        # Add the Handler to the Logger
        logger.addHandler(log_handler)
        return logger
       
    def _log_full_path(self):
        log_path = Path(self.log_path).resolve()
        log_path.mkdir(exist_ok=True)
        return  str(log_path / self.log_filename)      