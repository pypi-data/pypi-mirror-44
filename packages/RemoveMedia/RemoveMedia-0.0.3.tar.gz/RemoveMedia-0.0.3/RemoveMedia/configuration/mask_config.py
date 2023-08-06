from pathlib import Path
import pendulum

PARAMETERS = {
            "folder": {
                 "path" : {"default" : " ", "cli" : 'Path of folder(s) to remove content inside coma separated : ' },
                 "threshold_type" : {"default" : "weeks", "cli" : 'What units do you want to uses [weeks, days, hours, minutes, seconds] : '},
                 "threshold" : {"default" : "12", "cli" : "After how many time files or folder should be deleted : "},
            },
            "plex" : {
                "ip" : {"default" : " ", "cli" : 'Please enter your PMS IP Address (eg : 192.168.X.X) : '},
                "token" : {"default" : " ", "cli" : 'Please enter your PMS token : '},
                "link" : { "default" :  "http://${plex:IP}:32400/library/sections/all/refresh?X-Plex-Token=${plex:token}", "cli" : None}
            },
            "pushbullet" : {
                "api_key" : {"default" : " ", "cli" : 'Please enter your pushbullet API key : '},
            },
            "log" : {
                "log_path" : {"default" : str(Path(Path(__file__).parent.parent / "log").resolve()), "cli" : 'Please enter where to store log : ' },
                "log_filename" :  {"default" : f"{pendulum.now('UTC'):YYYYMMDD}_remove.log", "cli" : 'Please enter log filename : '},
            }        
        }