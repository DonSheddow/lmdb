import random
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import send_from_directory
from flask import jsonify

from lmdb import app
from lmdb import ffmpeg
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


@app.route('/media/test.mp4')
def media_test():
    start = request.args.get("start", 0)
    path = "/home/sheddow/Downloads/Mr.Robot.mkv"
    return Response(response=ffmpeg.transcode(path, start), mimetype='video/mp4', status=200)


@app.route('/media/duration.js')
def media_duration():
    path = "/home/sheddow/Downloads/Mr.Robot.mkv"
    return jsonify(duration=ffmpeg.get_duration(path))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
