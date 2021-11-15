import os
from config import db
from models import Director

DIRECTOR = [
    {'name': 'Raka', 'gender': 0, 'uid': 1, 'department':'Dpt WOW'},
    {'name': 'Riki', 'gender': 1, 'uid': 2, 'department':'Dpt WOW'},
    {'name': 'Wowo', 'gender': 2, 'uid': 3, 'department':'Dpt WOW'},
]

# Delete database file if it exists currently
if os.path.exists('database.db'):
    os.remove('database.db')

db.create_all()

# Iterate over the DIRECTOR structure and populate the database
for d in DIRECTOR:
    new_director = Director(
        name        = d['name'], 
        gender      = d['gender'],
        uid         = d['uid'],
        department  = d['department']
    )
    db.session.add(new_director)

db.session.commit()