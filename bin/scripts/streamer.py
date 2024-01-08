import os
import logging
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

concat_list_file = "concat_list.txt"
stream_process = None

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def start_rtsp_stream(ip_address):
    global stream_process
    # If a previous stream process exists, terminate it
    if stream_process and stream_process.poll() is None:
        stream_process.terminate()
        stream_process.wait()

    try:
        # Use the concat list file as input for FFmpeg with stream_loop option for infinite looping
        ffmpeg_command = [
            "ffmpeg",
            "-re",
            "-f", "concat",
            "-safe", "0",
            "-stream_loop", "-1",  # Loop indefinitely
            "-i", concat_list_file,
            "-c", "copy",
            "-f", "rtsp",
            f"rtsp://{ip_address}:8554/stream"  # Use provided IP address
        ]

        # Start FFmpeg process for streaming
        stream_process = subprocess.Popen(ffmpeg_command)
    except Exception as e:
        logging.error(f"Error encountered: {e}")

def restart_stream(event):
    if event.src_path == concat_list_file:
        logging.info("Detected changes in concat_list.txt. Restarting RTSP stream.")
        start_rtsp_stream(sys.argv[1])  # Pass the IP address as an argument

class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        restart_stream(event)

def monitor_concat_list_changes():
    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(concat_list_file), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

try:
    if len(sys.argv) != 2:
        print("Usage: python streamer.py <IP_ADDRESS>")
        sys.exit(1)
    start_rtsp_stream(sys.argv[1])  # Pass the IP address as an argument when starting
    monitor_concat_list_changes()
except KeyboardInterrupt:
    pass
