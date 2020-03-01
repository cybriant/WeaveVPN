from flask import Flask, jsonify, request, make_response
from werkzeug.security import gen_salt, generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims, current_user
)
from models import db, User
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'tRGeC9C8LjWab4wGRdhpqqHVqDCgpeTPKaEjtbNDyxTH8KhvkPhe2zpCuSjn2wecQdxqJCTeN67K7sN8m8wPQsHwxv4cWjXwkVvH'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=120)
jwt = JWTManager(app)
CORS(app)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    },
}

api = Api(app, security='Bearer Auth', authorizations=authorizations)

# ns_user = api.namespace('users', description='User management')


@app.before_first_request
def create_tables():
    db.create_all()

# Adds user identity information to JWT payload
@jwt.user_claims_loader
def add_claims_to_access_token(identity):

    user = User.query.filter_by(email=identity).first()

    return {
        'email': identity,
        'role': user.get_user_role(),
        'first_name': user.get_first_name(),
        'last_name': user.get_last_name(),
    }


@api.route('/register')
class Register(Resource):

    register_fields = api.model('Register', {
        'first_name': fields.String(description='First Name', required=True),
        'last_name': fields.String(description='Last Name', required=True),
        'email': fields.String(description='Email', required=True),
        'password': fields.String(description='Password', required=True),
    })

    @api.doc(body=register_fields, security=None)
    def post(self):
        """
        Register a new user
        """

        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter_by(email=email).first()

        # ANYONE WHO REGISTERS A NEW ACCOUNT WILL BE ASSIGNED AN ADMIN ROLE FOR NOW, THIS WILL NEED TO BE CHANGED IN THE FUTURE
        if not user:  # If no user exists with that email, then create account
            password_hashed = generate_password_hash(
                password=password, method="pbkdf2:sha256", salt_length=20)
            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=password_hashed, role='Administrator')
            db.session.add(user)
            db.session.commit()
            ret = {'access_token': create_access_token(email)}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 401)

# Admins can use this route to create a new user
@api.route('/add-user')
class AddUser(Resource):

    add_user_fields = api.model('Add User', {
        'first_name': fields.String(description='First Name', required=True),
        'last_name': fields.String(description='Last Name', required=True),
        'email': fields.String(description='Email', required=True),
        'role': fields.String(description='Password', required=True),
    })

    @api.doc(body=add_user_fields, security='Bearer Auth')
    @jwt_required
    def post(self):
        """
        Create a new user
        """

        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get('email')
        # this should be changed to a random password that is emailed to user later down the road
        password = 'password'
        role = request.json.get('role')

        user = User.query.filter_by(email=email).first()

        if not user:  # If no user exists with that email, then create account
            password_hashed = generate_password_hash(
                password=password, method="pbkdf2:sha256", salt_length=20)
            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=password_hashed, role=role)
            db.session.add(user)
            db.session.commit()
            ret = {'msg': 'Success'}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 401)

# Admins can use this route to edit/update a user
@api.route('/update-user')
class UpdateUser(Resource):

    update_user_fields = api.model('Update User', {
        'first_name': fields.String(description='First Name', required=True),
        'last_name': fields.String(description='Last Name', required=True),
        'email': fields.String(description='Email', required=True),
        'original_email': fields.String(description='Original email', required=True),
        'role': fields.String(description='Password', required=True),
    })

    @api.doc(body=update_user_fields, security='Bearer Auth')
    @jwt_required
    def put(self):
        """
        Update a user
        """

        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get('email')
        original_email = request.json.get('original_email')
        role = request.json.get('role')

        user = User.query.filter_by(email=original_email).first()

        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role
            db.session.commit()
            return make_response(jsonify({"msg": "Successfully updated user!"}), 200)
        else:
            ret = {'msg': 'User not found in database'}
            return make_response(jsonify(ret), 404)


# Admins can use this route to delete a user
@api.route('/delete-user/<email>')
@api.doc(params={'email': ''})
class DeleteUser(Resource):

    @api.doc(security='Bearer Auth')
    @jwt_required
    def delete(self, email):
        """
        Delete a user
        """

        user = User.query.filter_by(email=email).first()

        if not user:  # If no user exists with that email, then return error
            ret = {'msg': 'User not found in database'}
            return make_response(jsonify(ret), 404)

        else:
            db.session.delete(user)
            db.session.commit()
            ret = {'msg': 'Successfully deleted user'}
            return make_response(jsonify(ret), 200)


@api.route('/get-users')
class GetUsers(Resource):

    @api.doc(security='Bearer Auth')
    @jwt_required
    def get(self):
        """
        Returns a list of all users
        """

        # get all users from db
        users = User.query.all()

        # returns list of users
        return make_response(jsonify(users=[user.serialize() for user in users]))


@api.route('/login')
class Login(Resource):

    login_fields = api.model('Login', {
        'email': fields.String(description='Email', required=True),
        'password': fields.String(description='Password', required=True),
    })

    @api.doc(body=login_fields, security=None)
    def post(self):
        """
        Login a user
        """

        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter_by(email=email).first()

        # No user exists with the email address, return 401
        if not user:
            return make_response(jsonify({"msg": "Invalid credentials"}), 401)

        # if passwords match then log in, else return 401
        if(user.check_password(password)):
            ret = {'access_token': create_access_token(email)}
            return make_response(jsonify(ret), 200)
        else:
            return make_response(jsonify({"msg": "Invalid credentials"}), 401)


# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@api.route('/protected')
class TestProtectedMethod(Resource):

    @api.doc(security='Bearer Auth')
    @jwt_required
    def get(self):
        """
        Test protected route
        """
        claims = get_jwt_claims()
        return make_response(jsonify({
            'test': claims
        }), 200)


if __name__ == '__main__':
    app.run()
