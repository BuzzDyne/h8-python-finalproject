from flask import make_response, abort
from config import db
from models import Director, DirectorAndTheirMovieSchema, DirectorSchema, Movie, MovieAndItsDirectorSchema, MovieOnlySchema, MovieSchema
from utils import find_index
from operator import itemgetter

def read_all():
    """
    Read all Director entries on DB

    Returns
    -------
    list of DirectorSchema object
    """
    # Read all entries of Director ordered by its id
    dirs = Director.query.order_by(Director.id).limit(100)

    # Declare Schema to use (Passing many=True to indicate more than one object will be returned)   
    dir_schema = DirectorSchema(many=True)
    # Dumps the query result to Marshmello Schema for Serialization
    data = dir_schema.dump(dirs)
    return data

def read_with_movie_and_limit(limit):
    """
    Read Director entries on DB along with their movies, limited by the specified number

    Parameters
    ----------
    limit : int
        Number of items to retrieve. (0 means get all)

    Returns
    -------
    list of DirectorAndTheirMovieSchema object
    """
    # error validation for limit input
    if limit < 0:
        abort(400, f"Given Limit ({limit}) cannot be lower than 0")
    elif limit == 0:
        # if lower or equal to 0, query all Director
        dirs = Director.query.order_by(Director.id).all()
    else:
        # if higher than 0, query the first n Director
        dirs = Director.query.order_by(Director.id).limit(limit)
    
    # Declare Schema to use (Passing many=True to indicate more than one object will be returned)   
    dir_schema = DirectorAndTheirMovieSchema(many=True)
    # Dumps the query result to Marshmello Schema for Serialization
    data = dir_schema.dump(dirs)
    return data

def read_director_highest_revenue_budget_ratio(limit):
    """
    Read the first n Directors and then sorted by highest revenue/budget ratio on DB

    Parameters
    ----------
    limit : int
        Number of first n directors to be processed (0 means get all)

    Returns
    -------
    list of dict (Custom)
    """
    # prepare the result array
    res = []

    # error validation for limit input
    if limit < 0:
        abort(400, f"Given Limit ({limit}) cannot be lower than 0")
    elif limit == 0:
        # if lower or equal to 0, query all Director
        dirs = Director.query.all()
    else:
        # if higher than 0, query the first n Director
        dirs = Director.query.limit(limit)

    # For every director in the query result:
    for d in dirs:
        # Append an object and set its data
        res.append({
            'id'                : d.id,
            'name'              : d.name,
            'gender'            : d.gender,
            'total_budget'      : 0,
            'total_revenue'     : 0,
            'rev_bgt_ratio'     : 0,
            'rev_bgt_ratio_str' : ''
        })

        # Query all movies that was directed by current Director
        movs = Movie.query.filter(Movie.director_id == d.id)

        sum_budget  = 0
        sum_revenue = 0

        # Sum budget and revenue of each movie in the query result 
        for m in movs:
            sum_budget += m.budget
            sum_revenue += m.revenue

        # Find the index of current director's object in 'result' (list of dict)
        index = find_index(res, 'id', d.id)
        # Calculate Revenue/Budget ratio (if sum_budget is zero, set the ratio to zero, to avoid ZeroDivision)
        r_b_ratio = sum_revenue/sum_budget if sum_budget != 0 else 0

        # Set the sum_budget, sum_revenue and rev_bgt_ratio to the Director object
        res[index]['total_budget']      = sum_budget
        res[index]['total_revenue']     = sum_revenue
        res[index]['rev_bgt_ratio']     = round(r_b_ratio, 2)
        res[index]['rev_bgt_ratio_str'] = f"{round(r_b_ratio*100, 2)}%"

    # Sort the result list to be ordered by the highest ratio
    res = sorted(res, key=itemgetter('rev_bgt_ratio'), reverse=True)

    # Return the result (list of dict)
    return res

def read_by_id(dir_id):
    """
    Read a Director given its id

    Parameters
    ----------
    dir_id : int
        Id of the requested Director

    Returns
    -------
    DirectorSchema
    """
    # Perform the query
    dir = (
        Director.query.filter(Director.id == dir_id)
        .one_or_none()
    )

    # If query finds a Director of the given ID:
    if dir is not None:

        # Serialize the data for the response
        dir_schema = DirectorSchema()
        data = dir_schema.dump(dir)
        return data

    # Otherwise, send an error message
    else:
        abort(404, f"Director not found for Id: {dir_id}")

def create(dir):
    """
    Create a Director entry

    Parameters
    ----------
    dir : dict
        Data sent in the body of the request

    Returns
    -------
    (DirectorSchema, 201)
    """
    # Create a director instance using the schema and the passed in director
    schema = DirectorSchema()
    new_dir = schema.load(dir, session=db.session)

    # Add the director to the database
    db.session.add(new_dir)
    db.session.commit()

    # Serialize and return the newly created director in the response
    data = schema.dump(new_dir)

    return data, 201

def edit(dir_id, director):
    """
    Update a Director entry

    Parameters
    ----------
    dir_id : int
        Id of the Director to be updated
    dir : dict
        Data of the Director sent in the body of the request

    Returns
    -------
    (DirectorSchema, 201)
    """
    # Find the Director of the given dir_id
    update_director = Director.query.filter(
        Director.id == dir_id
    ).one_or_none()

    # If query finds a Director of the given ID:
    if update_director is not None:

        # turn the passed in director into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        # Set the id to the director we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return data, 202

    # Otherwise, send an error message
    else:
        abort(404, f"Director not found for Id: {dir_id}")

def delete(dir_id):
    """
    Delete a Director entry

    Parameters
    ----------
    dir_id : int
        Id of the Director to be deleted

    Returns
    -------
    (string, 200)
    """
    # Query the Director of the given dir_id
    dir = Director.query.filter(Director.id == dir_id).one_or_none()

    # If query finds a Director of the given ID:
    if dir is not None:
        # Delete the Director from DB
        db.session.delete(dir)
        db.session.commit()
        # Return response message to indicate successful operation
        return make_response(f"Director {dir_id} deleted", 200)

    # Otherwise, send an error message
    else:
        abort(404, f"Director not found for Id: {dir_id}")
