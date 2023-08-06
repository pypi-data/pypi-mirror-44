"""All function used for plex notification
"""
import urllib

def plex(plex_url, log, folder) -> None:
    """This function call given url
    Parameters
    --------------------
    plex_url : str
        url to open
     Returns
     ------------
     None
    """
    if plex_url:
        try:
            urllib.request.urlopen(plex_url, timeout=3)
        except urllib.error.HTTPError as error:
            log.info(f"unable to make request to Plex - HTTP Error {error.code}",
                     extra={"folder" : folder})
        except urllib.error.URLError as error:
            log.info(f"unable to make request to Plex - URL Error: {error.reason}",
                     extra={"folder" : folder})
        else:
            log.info(f"{plex_url} is refresh", extra={"folder" : folder})
             