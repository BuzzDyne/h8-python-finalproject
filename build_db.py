import os
from datetime import date
from config import db
from models import Director, Movie

DIRECTORS = [
    {'name': 'Raka', 'gender': 0, 'uid': 1, 'department':'Dpt WOW'},
    {'name': 'Riki', 'gender': 1, 'uid': 2, 'department':'Dpt WOW'},
    {'name': 'Wowo', 'gender': 2, 'uid': 3, 'department':'Dpt WOW'},
]

MOVIES = [
    {
        'original_title'      : "First Movie",
        'budget'              : 90000,
        'popularity'          : 60,
        'release_date'        : date(2021, 2, 27),
        'revenue'             : 2787965087,
        'title'               : "Avatar",
        'vote_average'        : 7.2,
        'vote_count'          : 11800,
        'overview'            : "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
        'tagline'             : "Enter the World of Pandora.",
        'uid'                 : 19995,
        'director_id'         : 1
    },
    {
        'original_title'      : "Second Movie",
        'budget'              : 90000,
        'popularity'          : 60,
        'release_date'        : date(2021, 5, 27),
        'revenue'             : 2787965087,
        'title'               : "Avatar 2",
        'vote_average'        : 7.2,
        'vote_count'          : 11800,
        'overview'            : "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
        'tagline'             : "Enter the World of Pandora.",
        'uid'                 : 19975,
        'director_id'         : 2
    }
]

# Delete database file if it exists currently
if os.path.exists('database.db'):
    os.remove('database.db')

db.create_all()

# Iterate over the DIRECTOR structure and populate the database
for m in DIRECTORS:
    new_movie = Director(
        name        = m['name'], 
        gender      = m['gender'],
        uid         = m['uid'],
        department  = m['department']
    )
    db.session.add(new_movie)

for m in MOVIES:
    new_movie = Movie(
        original_title      = m['original_title'],
        budget              = m['budget'],
        popularity          = m['popularity'],
        release_date        = m['release_date'],
        revenue             = m['revenue'],
        title               = m['title'],
        vote_average        = m['vote_average'],
        vote_count          = m['vote_count'],
        overview            = m['overview'],
        tagline             = m['tagline'],
        uid                 = m['uid'],
        director_id         = m['director_id']
    )
    db.session.add(new_movie)

db.session.commit()