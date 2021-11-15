from flask import make_response, abort
from config import db
from models import Director, DirectorSchema

def read_all():
    dirs = Director.query.order_by(Director.id).all()
    
    dir_schema = DirectorSchema(many=True)
    data = dir_schema.dump(dirs)
    return data

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