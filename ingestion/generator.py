import json
import os
from datetime import datetime
import time
import config

from event_builder import build_event

def generate_events():
   
    sleep_time = config.SLEEP_TIME
    
        
    while True:
        events = [build_event() for _ in range(config.BATCH_SIZE)]
        
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        
        path = f"{config.OUTPUT_PATH}/{year}/{month}/{day}/{hour}"
        if not os.path.exists(path):
            os.makedirs(path)
        
        file_path = f"{path}/events_{now.timestamp()}.jsonl"
        
        with open(file_path, "w") as f:
            for event in events:
                f.write(json.dumps(event) + "\n")
        time.sleep(sleep_time)
            

if __name__ == "__main__":
    generate_events()
            
        


   