from flask import make_response, abort
from config import db
from models import Director, DirectorMovieSchema, Movie, MovieSchema

def read_all():
    movs = Movie.query.order_by(Movie.id).all()
    
    mov_schema = DirectorMovieSchema(many=True)
    data = mov_schema.dump(movs)
    return data

def read_all_by_dirID(dir_id):
    movs = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == dir_id)
        .all()
    )

    mov_schema = DirectorMovieSchema(many=True)
    data = mov_schema.dump(movs)
    return data
