## -*- Code: Utf -*-

import os
import logging
from from_root import from_root
from datetime import datetime

'''creating Timestamp'''
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_dir = "logs"
'''joining paths from root'''
logs_path = os.path.join(from_root(),logs_dir,LOG_FILE)

'''create directory'''
os.makedirs(logs_dir,exist_ok=True)


'''config Logging Library'''
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

