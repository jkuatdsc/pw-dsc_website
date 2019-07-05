from flask import jsonify, make_response

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, jwt_refresh_token_required, get_jwt_identity, 
)    
from apps.accounts.models import User

parser = reqparse.RequestParser()
# Create a parser with shared arguments to be inherited
parser.add_argument(
    'username',
    required = True,
    help = 'Username attribute is required'
)
parser.add_argument(
    'password',
    required = True,
    help = 'Password attribute is required'
)

class Register(Resource):
    def post(self):
        reg_parser = parser.copy()
        reg_parser.add_argument(
            'email',
            required = True,
            help = 'Email attribute is required'
        )
        # Parse request data; return as dict
        data = reg_parser.parse_args()
        
        # Verify user with same username or email does not exist
        if User.objects(username=data['username']).first():
            return make_response(jsonify(
                msg='User %s already exists' % (data['username'])
            ), 400)
            
        elif User.objects(email=data['email']).first():
            return make_response(jsonify(
                msg='User with that email already exists'
            ), 400)

        new_user = User()
        new_user.email = data['email']
        new_user.username = data['username']
        new_user.password = data['password']
        new_user.save()

        return make_response(jsonify(
            msg='User created successfully'
        ), 201)


class Login(Resource):
    def post(self):
        data = parser.parse_args()
        # Get user 
        user = User.objects(username=data['username']).first()
        if not user:
            return make_response(jsonify(
                msg = 'User does not exist'
            ), 400)
        elif not user.verify_password(user.password_hash, data['password']):
            return make_response(jsonify(
                msg = 'You have entered wrong credentials, try again'
            ), 400)
        
        """
        Set the token as fresh to allow changing of critical information
        such as passwords, username etc. in a resource where stale tokens
        are rejected.
        """
        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)

        return make_response(jsonify(
            msg='You have logged in as %s' % (data['username']),
            access_token=access_token,
            refresh_token=refresh_token
        ), 302)


class RefreshAccessToken(Resource):
    """
    Create new access token (not fresh) for logged in users without them
    having to login again
    """
    @jwt_refresh_token_required
    def post(self):
        # Get the current logged in user
        current_user = get_jwt_identity()
        if not current_user:
            return make_response(jsonify(
                msg = 'You are not logged in'
            ), 401)
        
        new_access_token = create_access_token(
            identity=current_user,
            fresh=False
        )
        return make_response(jsonify(
            new_access_token = new_access_token
        ), 200)

