import random
from flask import Flask
from flask import render_template
from flask import request

from db import Session
from models import Media

app = Flask(__name__)

@app.route('/')
def main():
    session = Session()
    films = session.query(Media).all()
    
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
def film(id):
    session = Session()
    film = session.query(Media).filter_by(id=id).one()
    film.tmdb_rating = round(film.tmdb_rating, 1)
    
    return render_template('film.html', film=film)


@app.route('/search')
def search():
    session = Session()
    films = session.query(Media).all()[:5]
    
    return render_template('search.html', films=films)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
