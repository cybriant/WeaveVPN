from flask import Flask, jsonify, request
from werkzeug.security import gen_salt, generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims, current_user
)
from models import db, User
from models import OAuth2Token
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

@app.before_first_request
def create_tables():
    db.create_all()

# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):

    user = User.query.filter_by(email=identity).first()

    return {
        'email': identity,
        'role': user.get_user_role(),
        'first_name': user.get_first_name(),
        'last_name': user.get_last_name(),
    }

@app.route('/register', methods=['POST'])
def register():
    
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    # ANYONE WHO REGISTERS A NEW ACCOUNT WILL BE ASSIGNED AN ADMIN ROLE FOR NOW, THIS WILL NEED TO BE CHANGED IN THE FUTURE
    if not user: # If no user exists with that email, then create account
        password_hashed = generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=20)
        user = User(first_name=first_name, last_name=last_name, email=email,password=password_hashed,role='Administrator')
        db.session.add(user)
        db.session.commit()
        ret = {'access_token': create_access_token(email)}
        return jsonify(ret), 200

    else:
        return jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 401

# Admins can use this route to create a new user
@app.route('/add-user', methods=['POST'])
@jwt_required
def add_user():
    
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get('email')
    password = 'password' # this should be changed to a random password that is emailed to user later down the road
    role = request.json.get('role')

    user = User.query.filter_by(email=email).first()

    if not user: # If no user exists with that email, then create account
        password_hashed = generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=20)
        user = User(first_name=first_name, last_name=last_name, email=email, password=password_hashed, role=role)
        db.session.add(user)
        db.session.commit()
        ret = {'msg': 'Success'}
        return jsonify(ret), 200

    else:
        return jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 401

# Admins can use this route to delete a user
@app.route('/delete-user/<email>', methods=['DELETE'])
@jwt_required
def delete_user(email):

    user = User.query.filter_by(email=email).first()

    if not user: # If no user exists with that email, then return error
        ret = {'error': 'User not found'}
        return jsonify(ret), 404

    else:
        User.query.filter_by(email=email).delete()
        db.session.commit()
        ret = {'msg': 'Successfully deleted user'}
        return jsonify(ret), 204


@app.route('/get-users', methods=['GET'])
def get_users():
    
    # get all users from db
    users = User.query.all()

    # returns list of users
    return jsonify(users=[user.serialize() for user in users])


@app.route('/login', methods=['POST'])
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    # No user exists with the email address, return 401
    if not user:
        return jsonify({"msg": "User does not exists or invalid credentials"}), 401

    # if passwords match then log in, else return 401
    if(user.check_password(password)):
        ret = {'access_token': create_access_token(email)}
        return jsonify(ret), 200
    else:
        return jsonify({"msg": "User does not exists or invalid credentials"}), 401


# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    claims = get_jwt_claims()
    return jsonify({
        'test': claims
    }), 200


if __name__ == '__main__':
    app.run()
