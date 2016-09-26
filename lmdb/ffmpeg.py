import subprocess
import re
import os
from lmdb import app


def transcode(path, start):
    if not os.path.isfile(path):
        raise FileNotFoundError("No such file: '%s'" % path)
    cmdline = [app.config['FFMPEG']]
    cmdline.extend(app.config['FFMPEG_INPUT_ARGS'])
    cmdline.extend(['-ss', str(start), '-i', path])
    cmdline.extend(app.config['FFMPEG_OUTPUT_ARGS'])
    logfile = open('/tmp/lmdb_ffmpeg.log', 'w')
    proc = subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE,
            stderr=logfile)
    try:
        f = proc.stdout
        bytes_ = f.read(512)
        while bytes_:
            yield bytes_
            bytes_ = f.read(512)
    finally:
        proc.kill() 
        logfile.close()


FFPROBE = "ffprobe"
FFPROBE_DURATION = ['-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=p=0']

def get_duration(path):
    if not os.path.isfile(path):
        raise FileNotFoundError("No such file: '%s'" % path)

    cmdline = [FFPROBE, '-i', path]
    cmdline.extend(FFPROBE_DURATION)

    duration = -1
    proc = subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)
    try:
        output, _ = proc.communicate()
        duration = float(output)
    finally:
        proc.kill()

    return duration
