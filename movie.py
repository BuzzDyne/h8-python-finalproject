from flask import make_response, abort
from config import db
from models import Director, Movie, MovieAndItsDirectorSchema, MovieSchema, MovieOnlySchema

def read_all():
    movs = Movie.query.order_by(Movie.id).all()
    
    mov_schema = MovieOnlySchema(many=True)
    data = mov_schema.dump(movs)
    return data

def read_by_id(mov_id):
    mov = (
        Movie.query.filter(Movie.id == mov_id)
        .one_or_none()
    )

    # Did we find a person?
    if mov is not None:

        # Serialize the data for the response
        mov_schema = MovieSchema()
        data = mov_schema.dump(mov)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Movie not found for Id: {mov_id}")

def create(mov):
    # Create a person instance using the schema and the passed in person
    schema = MovieSchema()
    new_mov = schema.load(mov, session=db.session)

    # Add the person to the database
    db.session.add(new_mov)
    db.session.commit()

    # Serialize and return the newly created person in the response
    data = schema.dump(new_mov)

    return data, 201

def edit(mov_id, mov):
    update_mov = Movie.query.filter(
        Movie.id == mov_id
    ).one_or_none()

    # Did we find an existing person?
    if update_mov is not None:

        # turn the passed in person into a db object
        schema = MovieSchema()
        update = schema.load(mov, session=db.session)

        # Set the id to the person we want to update
        update.id = update_mov.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_mov)

        return data, 202

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Movie not found for Id: {mov_id}")

def delete(mov_id):
    mov = Movie.query.filter(Movie.id == mov_id).one_or_none()

    if mov is not None:
        db.session.delete(mov)
        db.session.commit()
        return make_response(f"Movie {mov_id} deleted", 200)

    else:
        abort(404, f"Movie not found for Id: {mov_id}")
