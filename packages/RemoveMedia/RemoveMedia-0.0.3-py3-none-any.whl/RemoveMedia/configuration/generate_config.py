from configparser import ConfigParser
from pathlib import Path
from RemoveMedia.configuration.mask_config import PARAMETERS
import pendulum

global CONFIG 

CONFIG_FOLDER = Path(Path(__file__).parent,  "config").resolve()

CONFIG = ConfigParser()


try:
    Now = pendulum.now()
except RuntimeError:
    Now = pendulum.now("UTC")
 
NAME = f"{Now:YYYYMMDDHHmmss}_default"

def generate_config(config_name : str = NAME, default=False) -> None:
    _create_folder()
    config_name = _create_filename(config_name)
    config_path = Path(CONFIG_FOLDER / config_name).resolve()
    if default:
        _param_by_default()
    else:
        _cli_generate_config()
    with open(config_path, 'w') as f:
        CONFIG.write(f)
    return config_name, config_path

def _create_filename(config_name : str) -> str:
    """return a properly formated config filename
    
    Arguments:
        config_name {str} -- filename
    
    Returns:
        str -- filename with .ini if not add in
    """
    if config_name:
        if '.ini' not in config_name:
            config_name = config_name + '.ini'
        return config_name
    return None

def _create_folder():
    if CONFIG_FOLDER.exists():
        pass
    else:
        CONFIG_FOLDER.mkdir()

def _cli_generate_config() -> None: #pragma: no cover
    print("We will generate a config file")
    _param_by_cli("folder")
    if _do_you_want("plex"):
        _param_by_cli("plex")
    if _do_you_want("pushbullet"):
        _param_by_cli("pushbullet")
    if _do_you_want("log"):
        _param_by_cli("log")         

def _do_you_want(name : str) -> bool:
    reponse = input(f'Do you want to add {name} parameters [y/n] : ')
    if reponse in ["yes", "y", "oui", "o", "ok"]:
        return True
    return False

def _param_by_cli(section : str) -> None:
    CONFIG[section] = {}
    for subsection, parameters in PARAMETERS[section].items():
        if parameters["cli"]:
            pcli = input(parameters["cli"])
            if pcli:
                CONFIG[section][subsection] = pcli
                continue            
        CONFIG[section][subsection] = parameters["default"]

def _param_by_default() -> None:
    for section, subsections in PARAMETERS.items():
        CONFIG[section] = {}
        for subsection, parameters in subsections.items():
            CONFIG[section][subsection] = parameters["default"]
  