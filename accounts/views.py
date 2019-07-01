from flask import jsonify, make_response

from flask_restful import Resource, reqparse

from accounts.models import User

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

