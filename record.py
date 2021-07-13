import subprocess
import time
import os
import sys
from datetime import date

global RECORDING_NUM
RECORDING_NUM = 1
STREAM_URL = sys.argv[1]  # input("URL: ")
NAME = sys.argv[2]  # input("Streamer: ")
QUALITY = "best"
RECORDINGS_FOLDER = "recordings"

ffmpeg_path = "ffmpeg"

SAVE_PATH = os.path.join(RECORDINGS_FOLDER, NAME)
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)


def ffmpeg_copy_and_fix_errors(recorded_filename, processed_filename):
    try:
        subprocess.call(
            [ffmpeg_path, "-err_detect", "ignore_err", "-i", recorded_filename, "-c", "copy",
                processed_filename])
        os.remove(recorded_filename)
        print("Processed file saved as {}".format(processed_filename))
    except Exception as e:
        print(e)


def start_recording(url, filename):
    global RECORDING_NUM
    subprocess.call(["streamlink", url, QUALITY, "-o", filename])
    if os.path.exists(filename) is True:
        print("Finished recording {}, now fixing.".format(filename))
        ffmpeg_copy_and_fix_errors(filename, filename.split(".mp4")[0] + "_processed.mp4")
        RECORDING_NUM += 1
        start_checking(10)


def check_online(url):
    return subprocess.call(['streamlink', url])


def get_stream_filename(name):
    global RECORDING_NUM
    today = date.today()
    filename = os.path.join(RECORDINGS_FOLDER, name, today.strftime(
        "%Y_%m_%d_{}_rec_{}.mp4".format(name, RECORDING_NUM)))
    while os.path.exists(filename) or os.path.exists(filename.split(".mp4")[0] + "_processed.mp4"):
        RECORDING_NUM += 1
        filename = os.path.join(RECORDINGS_FOLDER, name, today.strftime(
            "%Y_%m_%d_{}_rec_{}.mp4".format(name, RECORDING_NUM)))
    return filename


def start_checking(num_tries):
    while num_tries > 0:
        if check_online(STREAM_URL) == 0:
            # stream is online
            start_recording(STREAM_URL, get_stream_filename(NAME))
            sys.exit(0)
        else:
            # retry
            print("{} is offline. Waiting 5 seconds to retry...".format(STREAM_URL))
            num_tries -= 1
            time.sleep(5)
    print("Exceeded maximum number of attempts. Exiting...")
    sys.exit(0)


# start infinite loop of checks
start_checking(1000)
