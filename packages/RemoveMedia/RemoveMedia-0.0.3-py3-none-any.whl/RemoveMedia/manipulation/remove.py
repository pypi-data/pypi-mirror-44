from typing import Union, List, Tuple, Iterator, Optional, Dict

import pendulum
import shutil
import sys

from pathlib import Path
from time import ctime

from RemoveMedia.manipulation.base import Base

class Remove(Base):    
                   
    def delete(self
        ) -> None:
        """
        main entry point to remove file and folder
         Parameters
         -------------------
         treshold : int
             number to keep a file on the server
         folder : str
             path to folder you want to look for file to removed
         treshold_type : str
             specify type of treshold [years, months, weeks, days, hours, seconds, remaining_days, remaining_seconds]
         Returns
         -------------
         None    
        """
        for name, path in self._yield_folder_info():
            n_remove = 0
            list_remove = []
            for movie in path.iterdir():
                difference, is_difference = self._threshold_position(movie)
                if is_difference:
                    self.log.info(
                        f"{movie.name} is remove after {difference :.2f} {self.threshold_type} of existance",
                        extra={"folder" : name})
                    shutil.rmtree(movie.resolve())
                    n_remove += 1
                    list_remove.append(movie.name)
            self.log_notify(name, n_remove, list_remove)

    def log_notify(self, name, n_remove, list_remove) -> None:
        if not n_remove:
            self.log.info(
                "Nothing remove", 
                extra={"folder" : name}
                )
        else:
            self.log.info(
                f"{n_remove} files remove",
                extra={"folder" : name}
            )
            self._notify(name, n_remove, list_remove)

                                       
    def _threshold_position(self,
        file : Path
        ) -> Tuple[int, bool]:
        """get time delta between folder creation and threshold.
        Parameters
        -------------------
        file : Path
            file or folder to test
         threshold : int
             delta to compare
         threshold_type : str
             specify unit of delta value [years, months, weeks, days, hours, seconds, remaining_days, remaining_seconds]
         Returns
         -------------
         diff : int
             difference between today and folder creation date
          sup : bool
              if diff is supperior to threshold True else False 
        """
        file_stat = file.stat()
        create = pendulum.parse(ctime(file_stat.st_ctime), strict=False)
        diff = getattr(self.today - create, "total_" + self.threshold_type)()
        return diff, True if diff > self.threshold else False
                       