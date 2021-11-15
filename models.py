from config import db, ma

class Director(db.Model):
    __tablename__ = 'directors'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String)
    gender      = db.Column(db.Integer)
    uid         = db.Column(db.Integer)
    department  = db.Column(db.String)

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        sqla_session = db.session    
        load_instance = True