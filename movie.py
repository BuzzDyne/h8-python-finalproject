from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from flask import make_response, abort
from config import db
from models import Director, Movie, MovieAndItsDirectorSchema, MovieSchema

def read_all():
    """
    Read all Movie entries on DB

    Returns
    -------
    list of MovieSchema object
    """
    # Read all entries of Movie ordered by its id
    movs = Movie.query.order_by(Movie.id).limit(100)
    
    # Declare Schema to use (Passing many=True to indicate more than one object will be returned)   
    mov_schema = MovieSchema(many=True)
    # Dumps the query result to Marshmello Schema for Serialization
    data = mov_schema.dump(movs)
    return data

def read_with_director_and_limit(limit):
    """
    Read Movie entries on DB along with their director, limited by the specified number

    Parameters
    ----------
    limit : int
        Number of items to retrieve. (0 means get all)

    Returns
    -------
    list of MovieAndItsDirectorSchema object
    """
    # error validation for limit input
    if limit < 0:
        abort(400, f"Given Limit ({limit}) cannot be lower than 0")
    elif limit == 0:
        # if lower or equal to 0, query all Director
        movs = Movie.query.order_by(Movie.id).all()
    else:
        # if higher than 0, query the first n Director
        movs = Movie.query.order_by(Movie.id).limit(limit)
    
    # Declare Schema to use (Passing many=True to indicate more than one object will be returned)   
    mov_schema = MovieAndItsDirectorSchema(many=True)
    # Dumps the query result to Marshmello Schema for Serialization
    data = mov_schema.dump(movs)
    return data

def read_highest_revenue(limit):
    """
    Read n Movie of the higest revenue given the limit

    Parameters
    ----------
    limit : int
        Number of Movies (0 means get all)

    Returns
    -------
    List of MovieAndItsDirectorSchema
    """
    # error validation for limit input
    if limit < 0:
        abort(400, f"Given Limit ({limit}) cannot be lower than 0")
    elif limit == 0:
        # if lower or equal to 0, query all Director
        movs = Movie.query.order_by(Movie.revenue.desc()).all()
    else:
        # if higher than 0, query the first n Director
        movs = Movie.query.order_by(Movie.revenue.desc()).limit(limit)
    
    # Serialize the data for the response
    mov_schema = MovieAndItsDirectorSchema(many=True)
    data = mov_schema.dump(movs)
    return data

def read_movie_by_director_name(name):
    """
    Read All Movie by its director name

    Parameters
    ----------
    name : string
        Name of the requested Director

    Returns
    -------
    List of MovieAndItsDirectorSchema
    """
    try:
        # Query for the Director of the given name
        dir = Director.query.filter(Director.name == name).one()
    except NoResultFound:
        # If no Director found, return error message
        abort(404, f"No Director named ({name}) found!")
    
    # Query All movies which its director_id match to Director query result's id
    movs = Movie.query.filter(Movie.director_id == dir.id).all()
    
    # Serialize the data for the response
    mov_schema = MovieAndItsDirectorSchema(many=True)
    data = mov_schema.dump(movs)
    return data

def read_movie_sort_latest(limit):
    """
    Read n Movies sorted by the latest release date

    Parameters
    ----------
    limit : int
        Number of Movies (0 means get all)

    Returns
    -------
    List of MovieAndItsDirectorSchema
    """
    # error validation for limit input
    if limit < 0:
        abort(400, f"Given Limit ({limit}) cannot be lower than 0")
    elif limit == 0:
        # if lower or equal to 0, query all Movie sorted by its release_date
        movs = Movie.query.order_by(Movie.release_date.desc()).all()
    else:
        # if higher than 0, query the first n Movie sorted by its release_date
        movs = Movie.query.order_by(Movie.release_date.desc()).limit(limit)
    
    # Serialize the data for the response
    mov_schema = MovieSchema(many=True)
    data = mov_schema.dump(movs)
    return data

def read_by_id(mov_id):
    """
    Read a Movie given its id

    Parameters
    ----------
    mov_id : int
        Id of the requested Movie

    Returns
    -------
    MovieSchema
    """
    # Perform the query
    mov = (
        Movie.query.filter(Movie.id == mov_id)
        .one_or_none()
    )

    # If query finds a Director of the given ID:
    if mov is not None:

        # Serialize the data for the response
        mov_schema = MovieSchema()
        data = mov_schema.dump(mov)
        return data

    # Otherwise, send an error message
    else:
        abort(404, f"Movie not found for Id: {mov_id}")

def create(mov):
    """
    Create a Movie entry

    Parameters
    ----------
    mov : dict
        Data sent in the body of the request

    Returns
    -------
    (MovieSchema, 201)
    """
    # Create a movie instance using the schema and the passed in movie
    schema = MovieSchema()
    new_mov = schema.load(mov, session=db.session)

    # Add the movie to the database
    db.session.add(new_mov)
    db.session.commit()

    # Serialize and return the newly created movie in the response
    data = schema.dump(new_mov)

    return data, 201

def edit(mov_id, mov):
    """
    Update a Movie entry

    Parameters
    ----------
    mov_id : int
        Id of the Movie to be updated
    mov : dict
        Data of the Movie sent in the body of the request

    Returns
    -------
    (MovieSchema, 201)
    """
    # Find the Movie of the given dir_id
    update_mov = Movie.query.filter(
        Movie.id == mov_id
    ).one_or_none()

    # If query finds a Movie of the given ID:
    if update_mov is not None:

        # turn the passed in Movie into a db object
        schema = MovieSchema()
        update = schema.load(mov, session=db.session)

        # Set the id to the movie we want to update
        update.id = update_mov.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated movie in the response
        data = schema.dump(update_mov)

        return data, 202

    # Otherwise, send an error message
    else:
        abort(404, f"Movie not found for Id: {mov_id}")

def delete(mov_id):
    """
    Delete a Movie entry

    Parameters
    ----------
    dir_id : int
        Id of the Movie to be deleted

    Returns
    -------
    (string, 200)
    """
    # Query the Movie of the given dir_id
    mov = Movie.query.filter(Movie.id == mov_id).one_or_none()

    # If query finds a Movie of the given ID:
    if mov is not None:
        # Delete the Movie from DB
        db.session.delete(mov)
        db.session.commit()
        # Return response message to indicate successful operation
        return make_response(f"Movie {mov_id} deleted", 200)

    # Otherwise, send an error message
    else:
        abort(404, f"Movie not found for Id: {mov_id}")

def get_movies_by_dirID(dir_id):
    """
    Read All Movie by its director ID

    Parameters
    ----------
    dir_id : int
        ID of the requested Director

    Returns
    -------
    List of MovieAndItsDirectorSchema
    """
    try:
        # Query for the Director of the given id
        dir = Director.query.filter(Director.id == dir_id).one()
    except NoResultFound:
        # If no Director found, return error message
        abort(404, f"No Director of ID ({dir_id}) found!")
    
    # Query All movies which its director_id match to Director query result's id
    movs = Movie.query.filter(Movie.director_id == dir.id).all()
    
    # Serialize the data for the response
    mov_schema = MovieAndItsDirectorSchema(many=True)
    data = mov_schema.dump(movs)
    return data
