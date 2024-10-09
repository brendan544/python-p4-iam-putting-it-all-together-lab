#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe




class Signup(Resource):
     def post(self):
        data = request.get_json()

        # Validate the incoming data
        errors = {}
        
        # Required fields
        required_fields = ['username', 'password', 'image_url', 'bio']
        for field in required_fields:
            if field not in data:
                errors[field] = f"{field} is required."
        
        # Check for errors
        if errors:
            return jsonify({"errors": errors}), 422

        # Create the user
        new_user = User(
            username=data['username'],
            password=data['password'],  # This will trigger the password setter
            image_url=data['image_url'],
            bio=data['bio']
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id  # Store user ID in the session
            
            return jsonify({
                "id": new_user.id,
                "username": new_user.username,
                "image_url": new_user.image_url,
                "bio": new_user.bio
            }), 201

        except IntegrityError:
            db.session.rollback()  # Rollback if there's an error
            return jsonify({"errors": {"username": "Username already exists."}}), 422

class CheckSession(Resource):
      def get(self):
        # Check if the user is logged in
        user_id = session.get('user_id')

        if user_id:
            # Retrieve user details based on user_id
            user = User.query.get(user_id)  # Assuming you have the User model imported

            if user:
                return jsonify({
                    "id": user.id,
                    "username": user.username,
                    "image_url": user.image_url,
                    "bio": user.bio
                }), 200

        return jsonify({"error": "Unauthorized"}), 401


class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)