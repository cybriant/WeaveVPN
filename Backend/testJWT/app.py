from flask import Flask, jsonify, request
from werkzeug.security import gen_salt, generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)
from models import db, User
from models import OAuth2Token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'tRGeC9C8LjWab4wGRdhpqqHVqDCgpeTPKaEjtbNDyxTH8KhvkPhe2zpCuSjn2wecQdxqJCTeN67K7sN8m8wPQsHwxv4cWjXwkVvH'  # Change this!
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'email': identity,
        'role': 'Admin'
    }

@app.route('/register', methods=['POST'])
def register():
    
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # ANYONE WHO REGISTERS A NEW ACCOUNT WILL BE ASSIGNED AN ADMIN ROLE FOR NOW, THIS WILL NEED TO BE CHANGED IN THE FUTURE
    if not user: # If no user exists with that email, then create account
        password_hashed = generate_password_hash(password, method="pbkdf2:sha256", salt_length=20)
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
    
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get('email')
    password = 'password' # this should be changed to a random password that is emailed to user later down the road
    role = request.form.get('role')

    user = User.query.filter_by(email=email).first()

    if not user: # If no user exists with that email, then create account
        password_hashed = generate_password_hash(password, method="pbkdf2:sha256", salt_length=20)
        user = User(first_name=first_name, last_name=last_name, email=email, password=password_hashed, role=role)
        db.session.add(user)
        db.session.commit()
        ret = {'access_token': create_access_token(email)}
        return jsonify(ret), 200

    else:
        return jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 401


@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

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
        'test': 'success, this is a protected resource!'
    }), 200


if __name__ == '__main__':
    app.run()
