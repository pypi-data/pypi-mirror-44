from typing import Union

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from RemoveMedia.configuration.generate_config import _create_filename


class Reader:
    
    def __init__(self,  config_file_name : str):
        self.config_file_name =  config_file_name
        self.configuration = self.get_config_file

    @property
    def get_config_file(self) -> ConfigParser:
        config_file_name = _create_filename(self.config_file_name)
        if config_file_name:
            base_path = (Path(__file__).parent / 'config').resolve()
            file_path = base_path / config_file_name
            if file_path.exists():
                parser = ConfigParser(interpolation=ExtendedInterpolation())
                parser.read(file_path)
                return parser
            else:
                raise FileNotFoundError(f"Can't find this file : {config_file_name}")
        return None
   
    def select_value(self, 
        args : Union[str, int], 
        section : str, 
        descriptor : str,
        method : str = "get",
        fallbac : str = None
        ) -> None:
            """
           precedence function to return attribute : args > config > throw error
           Parameters
           --------------------
           args  : int, str, None
               args given 
            section : str
                section where descriptor should be inside
             descriptor : str
                  name inside the given session (cf_type)
             method : str
                 method use to grab descriptor value
             fallbac : str
                 default value to return if descriptor not in session
              Returns
              -------------
              Value : int, str, default
                  return approripruate value following this principle , args > config.
              Raise
              ---------
              NameError:
                  descriptor not found in args nor in config
           """
            if args:
                return args
            elif self.configuration:
                if section in self.configuration:
                    return getattr(self.configuration, method)(section, descriptor, fallback=fallbac)
                return fallbac
            return fallbac