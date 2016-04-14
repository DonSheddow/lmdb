from os.path import splitext

import requests

import data
import config
from models import Media, Movie, TV, Genre, Actor, Performance
from db import session_scope


def add_film_with_session(pathname, session):
    """Adds a film to the database, using the given session.

    This function looks at the pathname to determine the title
    and (optionally) the year of the film. Retrieves data via the
    data module, and adds the data along with the pathname
    to the database.
    """
    title = splitext(pathname)[0]
    d = data.search(title)

    if isinstance(d, data.MovieData):
        entry = Movie(pathname=pathname, **d.basic_info())
    else:
        entry = TV(pathname=pathname, **d.basic_info())

    for genre_name in d.genres():
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
        entry.genres.append(genre)

    # TODO: Remove duplicates from d.cast()
    # Test with add_film("Seven Samurai")
    for order, actor_name, role in d.cast():
        with session.no_autoflush:
            actor = session.query(Actor).filter_by(name=actor_name).first()
            if not actor:
                actor = Actor(name=actor_name)

            performance = Performance(role=role)
            performance.actor = actor
            entry.performances.append(performance)
        session.flush()

    session.add(entry)

    url = d.poster_url()
    r = requests.get(url)
    r.raise_for_status()

    session.commit()
    with open(config.IMAGE_DIR + '/%s.jpg' % entry.id, 'wb') as f:
        f.write(r.content)


def add_film(pathname):
    """Adds a film to the database.

    Creates a new session s, then calls
    add_film_with_session(pathname, s)
    """
    with session_scope() as session:
        add_film_with_session(pathname, session)


def remove_film_with_session(pathname, session):
    entry = session.query(Media).filter_by(pathname=pathname).one()
    session.delete(entry)

def remove_film(pathname):
    with session_scope() as session:
        remove_film_with_session(pathname, session)


