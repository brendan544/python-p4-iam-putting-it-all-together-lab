from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    _password_hash = Column(String(128), nullable=False)
    image_url = Column(String(256))
    bio = Column(String(512))

    recipes = relationship('Recipe', back_populates='author')

    @property
    def password_hash(self):
        raise AttributeError("Password hash is not accessible.")

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must not be empty.")
        return username

    @property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    instructions = Column(String, nullable=False)
    minutes_to_complete = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='recipes')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title must not be empty.")
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if len(instructions) < 50:
            raise ValueError("Instructions must be at least 50 characters long.")
        return instructions








