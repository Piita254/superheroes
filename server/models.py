from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData() 

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model,SerializerMixin):
    __tablename__ = 'heroes' 

    serialize_rules = ('-superHero.hero',)

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    superheros = db.relationship('SuperHero',back_populates='hero')

class Power(db.Model,SerializerMixin):
    __tablename__='powers'

    serialize_rules = ('-superhero.power')
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String)

    superheros = db.relationship('SuperHero',back_populates='power')

class SuperHero(db.Model,SerializerMixin):
    __tablename__= 'super_heros'

    serialize_rules = ('-hero.superhero','-power.superhero')

    id = db.Column(db.Integer,primary_key=True)
    strength = db.Column(db.Integer)
    hero_id = db.Column(db.Integer,db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer,db.ForeignKey('powers.id'))
    
    hero = db.relationship('Hero',back_populates = 'superheros')
    power = db.relationship('Power',back_populates='superheros')






