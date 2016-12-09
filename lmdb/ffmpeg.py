import subprocess
import os
from lmdb import app


def transcode(path, start):
    if not os.path.isfile(path):
        raise FileNotFoundError("No such file: '%s'" % path)
    cmd = [app.config['FFMPEG']]
    cmd.extend(app.config['FFMPEG_INPUT_ARGS'])
    cmd.extend(['-ss', str(start), '-i', path])
    cmd.extend(app.config['FFMPEG_OUTPUT_ARGS'])
    logfile = open('/tmp/lmdb_ffmpeg.log', 'w')
    proc = subprocess.Popen(
            cmd,
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

    cmd = [FFPROBE, '-i', path]
    cmd.extend(FFPROBE_DURATION)

    duration = -1
    proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)
    try:
        output, _ = proc.communicate()
        duration = float(output)
    finally:
        proc.kill()

    return duration
