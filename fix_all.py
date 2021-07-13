import glob
import subprocess
import os

QUALITY = "best"
RECORDINGS_FOLDER = "recordings/"

ffmpeg_path = "ffmpeg"


def ffmpeg_copy_and_fix_errors(recorded_filename, processed_filename):
    try:
        subprocess.call(
            [ffmpeg_path, "-err_detect", "ignore_err", "-i", recorded_filename, "-c", "copy",
                processed_filename])
        os.remove(recorded_filename)
        print("Processed file saved as {}".format(processed_filename))
    except Exception as e:
        print(e)


def walk():
    for filename in glob.iglob(RECORDINGS_FOLDER + '**/*.mp4', recursive=True):
        print("Checking {}".format(filename))
        if not "processed" in filename:
            ffmpeg_copy_and_fix_errors(filename, filename.split(".mp4")[
                                       0] + "_processed.mp4")

if __name__ == "__main__":
    walk()