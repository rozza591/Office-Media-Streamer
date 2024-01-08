import time
import os
import subprocess
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.abspath(os.path.join(script_dir, '../../input'))
processing = os.path.abspath(os.path.join(script_dir, '../../processing'))
output_folder = os.path.abspath(os.path.join(script_dir, '../../ts'))
ffmpeg_path = os.path.abspath(os.path.join(script_dir, '../ffmpeg'))

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.mp4', '.avi', '.mkv')):
            input_file = event.src_path
            output_file = os.path.join(processing, os.path.splitext(os.path.basename(input_file))[0] + ".ts")
            convert_to_ts(input_file, output_file)

def convert_to_ts(input_file, output_file):
    ffmpeg_exec = os.path.join(ffmpeg_path, "ffmpeg")
    cmd = [ffmpeg_exec, "-i", input_file, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", output_file]
    subprocess.run(cmd)

    # Move the file to the output_folder after transcoding
    output_file_final = os.path.join(output_folder, os.path.basename(output_file))
    shutil.move(output_file, output_file_final)
    print(f"Transcoding finished: {output_file_final}")

if __name__ == "__main__":
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, input_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
