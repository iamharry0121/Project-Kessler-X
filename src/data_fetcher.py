import os
import urllib.request
import time
import datetime
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = Path(BASE_DIR, 'data')
DATA_DIR.mkdir(parents=True, exist_ok=True)
c_epoch_time = int(time.time())
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

URL_MAP = {
    'active_satellites': 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=csv',
    'iridium_debris': 'https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium-33-debris&FORMAT=csv',
    'cosmos_debris': 'https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-2251-debris&FORMAT=csv'
}

def fileModTime(dir_to_check):
    final_times = {}
    for file in dir_to_check.iterdir():
        if file.is_file():
            file_m_time = file.stat().st_mtime
            final_times.update({file.stem:file_m_time})
            
    return(final_times)

def fileNeedsUpdate(current_time, f_name):
    mod_times = fileModTime(DATA_DIR)
    if f_name not in mod_times:
        return True  #file doesn't exist, needs download
    age_in_seconds = current_time - mod_times[f_name]
    if age_in_seconds > 12600: #12600 being 3.5 hours in seconds
        return True
    
    return False
        

for key,value in URL_MAP.items():
    if fileNeedsUpdate(c_epoch_time, key) == True:
        f_location = DATA_DIR / f'{key}.csv'
        with urllib.request.urlopen(value) as response:
            r_holder = response.read()
            with open(f_location, 'wb') as file:
                file.write(r_holder)
                print(f'Successfully downloaded {key}!')
                time.sleep(3)
    else:
        print(f"Skipping {key} - local copy is already fresh.")





