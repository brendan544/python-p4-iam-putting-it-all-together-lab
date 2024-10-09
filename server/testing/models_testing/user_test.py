from sqlalchemy.exc import IntegrityError
import pytest

from app import app
from models import db, User, Recipe

class TestUser:
    '''User in models.py'''

   
   
   
   
   

    def test_requires_username(self):
        '''requires each record to have a username.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user = User()
            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_unique_username(self):
        '''requires each record to have a username.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user_1 = User(username="Ben")
            user_2 = User(username="Ben")

            with pytest.raises(IntegrityError):
                db.session.add_all([user_1, user_2])
                db.session.commit()

    
    

    

    
    

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     
     
    
    
    

    
    

    
    

    
    
    
    

    
    
    