import glob
import subprocess
import os
import threading
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

QUALITY = "best"
RECORDINGS_FOLDER = "recordings/"

ffmpeg_path = "ffmpeg"


def ffmpeg_copy_and_fix_errors(recorded_filename, processed_filename):
    try:
        subprocess.call(
            [ffmpeg_path, "-err_detect", "ignore_err", "-i", recorded_filename, "-c", "copy",
                processed_filename])
        os.remove(recorded_filename)
        logging.info("Processed file saved as {}".format(processed_filename))
    except Exception as e:
        logging.error(e)


def walk():
    jobs = []
    for filename in glob.iglob(RECORDINGS_FOLDER + '**/*.mp4', recursive=True):
        logging.info("Checking {}".format(filename))
        if not "processed" in filename:
            x = threading.Thread(target=ffmpeg_copy_and_fix_errors, args=(
                filename, filename.split(".mp4")[0] + "_processed.mp4"))
            logging.info("Fixing errors in {}".format(filename))
            x.start()
            jobs.append(x)
            # ffmpeg_copy_and_fix_errors(filename, filename.split(".mp4")[0] + "_processed.mp4")
    
    for job in jobs:
        job.join()
    logging.info("Finished.")


if __name__ == "__main__":
    walk()
