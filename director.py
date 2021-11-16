from flask import make_response, abort
from config import db
from models import Director, DirectorMovieSchema, DirectorSchema, Movie, MovieDirectorSchema

def read_all():
    dirs = Director.query.order_by(Director.id).all()
    
    dir_schema = MovieDirectorSchema(many=True)
    data = dir_schema.dump(dirs)
    return data

def read_by_id(dir_id):
    dir = (
        Director.query.filter(Director.id == dir_id)
        .outerjoin(Movie)
        .one_or_none()
    )

    # Did we find a person?
    if dir is not None:

        # Serialize the data for the response
        dir_schema = DirectorSchema()
        data = dir_schema.dump(dir)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {dir_id}")


def create(dir):
    # Create a person instance using the schema and the passed in person
    schema = DirectorSchema()
    new_dir = schema.load(dir, session=db.session)

    # Add the person to the database
    db.session.add(new_dir)
    db.session.commit()

    # Serialize and return the newly created person in the response
    data = schema.dump(new_dir)

    return data, 201

def edit(dir_id, director):
    update_director = Director.query.filter(
        Director.id == dir_id
    ).one_or_none()

    # Did we find an existing person?
    if update_director is not None:

        # turn the passed in person into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the person we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Director not found for Id: {dir_id}")

def delete(dir_id):
    dir = Director.query.filter(Director.id == dir_id).one_or_none()

    if dir is not None:
        db.session.delete(dir)
        db.session.commit()
        return make_response(f"Director {dir_id} deleted", 200)

    else:
        abort(404, f"Person not found for Id: {dir_id}")
