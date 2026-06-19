import urllib.request
import urllib.error
import time
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(BASE_DIR, 'data')
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = Path(BASE_DIR) / 'config' / 'settings.json'

with open(CONFIG_PATH, 'r') as config_file:
    data_needed = json.load(config_file)

def fileModTime(dir_to_check):
    final_times = {}
    for file in dir_to_check.iterdir():
        if file.is_file():
            file_m_time = file.stat().st_mtime
            final_times.update({file.stem:file_m_time})
            
    return(final_times)

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)


def fileNeedsUpdate(current_time, f_name, mod_times):
    if f_name not in mod_times:
        return True  #file doesn't exist, needs download
    age_in_seconds = current_time - mod_times[f_name]
    if age_in_seconds > data_needed['cache_threshold_seconds']: #12600 being 3.5 hours in seconds
        return True
    
    return False
        
def runDataUpdate():
    c_epoch_time = int(time.time())
    all_mod_times = fileModTime(DATA_DIR)  

    for key, value in data_needed['data_sources'].items():
        if fileNeedsUpdate(c_epoch_time, key, all_mod_times) == True:
            f_location = DATA_DIR / f'{key}.csv'
            try:
                with urllib.request.urlopen(value) as response:
                    r_holder = response.read()
                    with open(f_location, 'wb') as file:
                        file.write(r_holder)
                        print(f'Successfully downloaded {key}!')
            except urllib.error.HTTPError as e:
                print(f'Failed to download {key}: HTTP {e.code} - {e.reason}')
                if e.code == 403:
                    body = e.read().decode('utf-8', errors='replace')
                    print(f'Server says: {body[:200]}')
            except urllib.error.URLError as e:
                print(f'Network error downloading {key}: {e.reason}')
            except Exception as e:
                print(f'Unexpected error downloading {key}: {e}')
            finally:
                time.sleep(3)
        else:
            print(f"Skipping {key} - local copy is already fresh.")





