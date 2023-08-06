from typing import List

from pushbullet import Pushbullet, InvalidKeyError
 
def pbullet(
        pb_api_key : str,
        name : str,
        n_remove : str,
        list_remove : List[str], 
        log,
        ) -> None:
        """
        Send notification via pushbullet
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
        try:
            pb = Pushbullet(pb_api_key)
            body = "List of removed files : \n"
            for fname in list_remove:
                body += f" - {fname} \n"
            push = pb.push_note( f"In folder {name} {n_remove} files has been removed", body)
            log.info(f"pushbullet notify",  extra={"folder" : name})           
        except InvalidKeyError as e:
             log.info(f"Your key is not valid",  extra={"folder" : name})