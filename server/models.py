from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-superheroes.hero',)  # Avoid circular serialization

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship to SuperHero (Hero to SuperHero is One-to-Many)
    superheroes = db.relationship('SuperHero', back_populates='hero')


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-superheroes.power',)  # Avoid circular serialization
    name = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    # Relationship to SuperHero (Power to SuperHero is One-to-Many)
    superheroes = db.relationship('SuperHero', back_populates='power')


class SuperHero(db.Model, SerializerMixin):
    __tablename__ = 'superheroes'  # Correct plural form of the table name

    serialize_rules = ('-hero.superheroes', '-power.superheroes')  # Avoid circular serialization

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Integer)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # Many-to-One relationships to Hero and Power
    hero = db.relationship('Hero', back_populates='superheroes')
    power = db.relationship('Power', back_populates='superheroes')
