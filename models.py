from sqlalchemy.orm import relationship
from config import db, ma
from marshmallow import fields

class Director(db.Model):
    __tablename__ = 'directors'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String)
    gender      = db.Column(db.Integer)
    uid         = db.Column(db.Integer)
    department  = db.Column(db.String)

    movies = relationship("Movie")

class Movie(db.Model):
    __tablename__ = 'movies'
    id                  = db.Column(db.Integer, primary_key=True)
    original_title      = db.Column(db.String)
    budget              = db.Column(db.Integer)
    popularity          = db.Column(db.Integer)
    release_date        = db.Column(db.Date)
    revenue             = db.Column(db.Integer)
    title               = db.Column(db.String)
    vote_average        = db.Column(db.Float)
    vote_count          = db.Column(db.Integer)
    overview            = db.Column(db.String)
    tagline             = db.Column(db.String)
    uid                 = db.Column(db.Integer)

    director_id         = db.Column(db.Integer, db.ForeignKey('directors.id'))
    director            = relationship("Director", back_populates="movies")

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        sqla_session = db.session
        load_instance = True

class DirectorAndTheirMovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Director
        sqla_session = db.session    
        load_instance = True

    movies = fields.Nested('MovieOnlySchema', default=[], many=True)

class MovieOnlySchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id                  = fields.Int()
    original_title      = fields.Str()
    budget              = fields.Int()
    popularity          = fields.Int()
    release_date        = fields.Date()
    revenue             = fields.Int()
    title               = fields.Str()
    vote_average        = fields.Float()
    vote_count          = fields.Int()
    overview            = fields.Str()
    tagline             = fields.Str()
    uid                 = fields.Int()
    director_id         = fields.Int()

class MovieSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        sqla_session = db.session
        include_fk = True
        load_instance = True

class MovieAndItsDirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movie
        sqla_session = db.session

    director = fields.Nested("DirectorOnlySchema", default=None)

class DirectorOnlySchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id          = fields.Int()
    name        = fields.Str()
    gender      = fields.Int()
    uid         = fields.Int()
    department  = fields.Str()