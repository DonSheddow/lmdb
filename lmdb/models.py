from lmdb import db

media_genres = db.Table('media_genres',
    db.Column('media_id', db.Integer, db.ForeignKey('media.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
)


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    
    def __repr__(self):
        return "<Genre('%s')>" % self.name


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    
    def __repr__(self):
        return "<Actor('%s')>" % self.name



class Performance(db.Model):
    __tablename__ = 'performances'
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), primary_key=True)
    role = db.Column(db.String)
    actor = db.relationship("Actor", backref="performances")
    
    def __repr__(self):
        return "<Performance('%s', '%s')" % (self.actor.name, self.role)
    


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    pathname = db.Column(db.String, index=True, unique=True)
    title = db.Column(db.String)
    summary = db.Column(db.String)
    tmdb_rating = db.Column(db.Float)
    
    genres = db.relationship('Genre', secondary=media_genres, backref='media')
    
    performances = db.relationship("Performance")
    
    type = db.Column(db.String(32))
    
    __mapper_args__ = {
        'polymorphic_on': type
    }



class Movie(Media):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'movie'
    }
    
    def __repr__(self):
        return "<Movie('%s')>" % self.title


class TV(Media):
    __tablename__ = 'tv'
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'tv'
    }
    
    def __repr__(self):
        return "<TV('%s')>" % self.title
