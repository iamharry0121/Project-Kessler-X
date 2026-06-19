import torch
import json
from data_fetcher import BASE_DIR, runDataUpdate
from pathlib import Path

CONFIG_PATH = Path(BASE_DIR) / 'config' / 'settings.json'
active_engine = 'cpu'

with open(CONFIG_PATH, 'r') as config_file:
    data_needed = json.load(config_file)

runDataUpdate()

if data_needed['execution_mode'] == 'auto':
    if torch.cuda.is_available() == True:
        active_engine = 'gpu'
    elif torch.backends.mps.is_available() == True:
        active_engine = 'npu'
    else:
        active_engine = 'cpu'





