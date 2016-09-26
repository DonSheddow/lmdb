import random
import re
import subprocess
import time
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask import jsonify

from lmdb import app
from lmdb.models import Media

@app.route('/')
def main():
    films = Media.query.all()

    for film in films:
        film.tmdb_rating = round(film.tmdb_rating, 1)

    random.shuffle(films)
    favorites = films[:5]
    random.shuffle(films)
    recently_viewed = films[:5]
    random.shuffle(films)
    recently_added = films[-5:]

    return render_template('index.html', favorites=favorites, recently_viewed=recently_viewed, recently_added=recently_added)


@app.route('/film/<id>')
def film(id): # pylint: disable=invalid-name
    film = Media.query.get_or_404(id)
    film.tmdb_rating = round(film.tmdb_rating, 1)

    return render_template('film.html', film=film)


@app.route('/search')
def search():
    title = request.args.get('title', '')
    films = Media.query.filter(Media.title.ilike("%{}%".format(title))).all()

    # Presumptuous to redirect?
    # https://ux.stackexchange.com/questions/76575/should-i-redirect-the-user-if-theres-only-one-search-result-or-still-show-the
    if len(films) == 1 and films[0].title.lower() == title.lower():
        return redirect(url_for('film', id=films[0].id))

    return render_template('search.html', films=films)


@app.route('/media/test.ogv')
def media_test():
    start = request.args.get("start", 0)
    path = "/home/sheddow/Downloads/Mr.Robot.mkv"
    def generate():
        cmdline = [app.config['FFMPEG']]
        cmdline.extend(app.config['FFMPEG_INPUT_ARGS'])
        cmdline.extend(['-ss', str(start), '-i', path])
        cmdline.extend(app.config['FFMPEG_OUTPUT_ARGS'])
        f = open('/tmp/ffmpeg.log', 'w')
        proc = subprocess.Popen(
                cmdline,
                stdout=subprocess.PIPE,
                stderr=f)
        try:
            f = proc.stdout
            b = f.read(512)
            while b:
                yield b
                b = f.read(512)
        finally:
            proc.kill()
            f.close()

    return Response(response=generate(), mimetype='video/mp4', status=200)


@app.route('/media/duration.js')
def media_duration():
    path = "/home/sheddow/Downloads/Mr.Robot.mkv"
    cmdline = [app.config['FFMPEG'], '-i', path]
    duration = -1
    proc = subprocess.Popen(
            cmdline,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE)
    try:
        for line in iter(proc.stderr.readline, ''):
            line = line.rstrip()
            m = re.search(b'Duration: (..):(..):(..)\...', line)
            if m is not None:
                duration = int(m.group(1)) * 3600 + int(m.group(2))*60 + int(m.group(3)) + 1
                break
    finally:
        proc.kill()

    return jsonify(duration=duration)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
