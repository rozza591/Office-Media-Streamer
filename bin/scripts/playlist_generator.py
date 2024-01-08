import os
import logging
import time
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

script_dir = os.path.dirname(os.path.abspath(__file__))
ts_folder = os.path.abspath(os.path.join(script_dir, '../../ts'))
concat_list_file = "concat_list.txt"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def update_concat_list(ts_files):
    if not ts_files:
        logging.warning("No TS files found.")
        return

    # Randomize the list of TS files
    random.shuffle(ts_files)

    # Update the concat_list.txt file with TS file entries
    with open(concat_list_file, "w") as file:
        for ts_file in ts_files:
            file.write(f"file '{os.path.join(ts_folder, ts_file)}'\n")
        logging.info("Concat list updated and randomized.")

# Initial concat list creation
initial_ts_files = [f for f in os.listdir(ts_folder) if f.endswith(".ts")]
update_concat_list(initial_ts_files)

class FileModifiedHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.src_path.endswith(".ts"):
            logging.info(f"Detected changes in TS folder. Updating concat list.")
            ts_files = [f for f in os.listdir(ts_folder) if f.endswith(".ts")]
            update_concat_list(ts_files)

# Watchdog setup to monitor changes in the TS folder
event_handler = FileModifiedHandler()
observer = Observer()
observer.schedule(event_handler, ts_folder, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    observer.stop()
observer.join()
