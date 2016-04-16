from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table

Base = declarative_base()

media_genres = Table('media_genres', Base.metadata,
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True, unique=True)
    
    def __repr__(self):
        return "<Genre('%s')>" % self.name


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    
    def __repr__(self):
        return "<Actor('%s')>" % self.name



class Performance(Base):
    __tablename__ = 'performances'
    media_id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)
    role = Column(String)
    actor = relationship("Actor", backref="performances")
    
    def __repr__(self):
        return "<Performance('%s', '%s')" % (self.actor.name, self.role)
    


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    pathname = Column(String, index=True, unique=True)
    title = Column(String)
    summary = Column(String)
    tmdb_rating = Column(Float)
    
    genres = relationship('Genre', secondary=media_genres, backref='media')
    
    performances = relationship("Performance")
    
    type = Column(String(32))
    
    __mapper_args__ = {
        'polymorphic_on': type
    }



class Movie(Media):
    __tablename__ = 'movies'
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'movie'
    }
    
    def __repr__(self):
        return "<Movie('%s')>" % self.title


class TV(Media):
    __tablename__ = 'tv'
    id = Column(Integer, ForeignKey('media.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'tv'
    }
    
    def __repr__(self):
        return "<TV('%s')>" % self.title
