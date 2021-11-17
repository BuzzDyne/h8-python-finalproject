from flask import make_response, abort
from config import db
from models import Director, DirectorAndTheirMovieSchema, DirectorSchema, Movie, MovieAndItsDirectorSchema, MovieOnlySchema, MovieSchema
from utils import find_index
from operator import itemgetter

def read_all():
    dirs = Director.query.order_by(Director.id).all()
    
    dir_schema = DirectorSchema(many=True)
    data = dir_schema.dump(dirs)
    return data

def read_with_movie_and_limit(limit):
    dirs = Director.query.order_by(Director.id).limit(limit)
    
    dir_schema = DirectorAndTheirMovieSchema(many=True)
    data = dir_schema.dump(dirs)
    return data

def read_summary_financial(limit):
    res = []

    if limit <= 0:
        dirs = Director.query.all()
    else:
        dirs = Director.query.limit(limit)

    for d in dirs:
        res.append({
            'id'                : d.id,
            'name'              : d.name,
            'gender'            : d.gender,
            'total_budget'      : 0,
            'total_revenue'     : 0,
            'rev_bgt_ratio'     : 0,
            'rev_bgt_ratio_str' : ''
        })

        movs = Movie.query.filter(Movie.director_id == d.id)

        sum_budget  = 0
        sum_revenue = 0

        for m in movs:
            sum_budget += m.budget
            sum_revenue += m.revenue

        index = find_index(res, 'id', d.id)
        r_b_ratio = sum_revenue/sum_budget if sum_budget != 0 else 0
        res[index]['total_budget']      = sum_budget
        res[index]['total_revenue']     = sum_revenue
        res[index]['rev_bgt_ratio']     = round(r_b_ratio, 2)
        res[index]['rev_bgt_ratio_str'] = f"{round(r_b_ratio*100, 2)}%"

    res = sorted(res, key=itemgetter('rev_bgt_ratio'), reverse=True)

    return res

def read_by_id(dir_id):
    dir = (
        Director.query.filter(Director.id == dir_id)
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

        return data, 202

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
        abort(404, f"Director not found for Id: {dir_id}")

def get_movies_by_dirID(dir_id):
    movs = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == dir_id)
        .all()
    )

    movs = (
        Movie.query.join(Director, Director.id == Movie.director_id)
        .filter(Director.id == dir_id)
        .all()
    )

    mov_schema = MovieOnlySchema(many=True)
    data = mov_schema.dump(movs)
    return data