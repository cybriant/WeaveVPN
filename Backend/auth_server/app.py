from flask import Flask, jsonify, request, make_response, send_file
from werkzeug.security import gen_salt, generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims, current_user
)
from models import db, User, ServerGroup, Organization, Network, Connection
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
import uuid
# from abc import ABC, abstractmethod
import datetime

from zipfile import ZipFile


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

ns_network = api.namespace(
    'network', description='API calls for networks'
)

ns_server_group = api.namespace(
    'server-group', description='API calls for server groups')

ns_organization = api.namespace(
    'organization', description='API calls for organizations'
)

ns_connection = api.namespace(
    'connection', description="API calls for connections"
)


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

# End point to download zip file
@api.route('/download')
class Download(Resource):

    def get(self):

        # Add name of the zip file to go here
        path = "configuration.zip"

        return send_file(path, as_attachment=True)


@api.route('/create_zip')
class CreateZip(Resource):
    def get(self):
        # create a ZipFile object
        zipObj = ZipFile('configuration.zip', 'w')

        # Add multiple files to the zip
        zipObj.write('open-vpn-command.py')

        # close the Zip File
        zipObj.close()

        return make_response(jsonify({"msg": "Successfully Created Zip"}), 200)


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

        id = request.json.get("id")
        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get('email')
        password = request.json.get('password')

        user = User.query.filter_by(email=email).first()

        # ANYONE WHO REGISTERS A NEW ACCOUNT WILL BE ASSIGNED AN ADMIN ROLE FOR NOW, THIS WILL NEED TO BE CHANGED IN THE FUTURE
        if not user:  # If no user exists with that email, then create account
            password_hashed = generate_password_hash(
                password=password, method="pbkdf2:sha256", salt_length=20)
            user = User(id=id, first_name=first_name, last_name=last_name,
                        email=email, password=password_hashed, role='Administrator')
            db.session.add(user)
            db.session.commit()
            ret = {'access_token': create_access_token(email)}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 401)


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

# Admins can use this route to create a new user
@api.route('/add-user')
class AddUser(Resource):

    add_user_fields = api.model('Add User', {
        'first_name': fields.String(description='First Name', required=True),
        'last_name': fields.String(description='Last Name', required=True),
        'email': fields.String(description='Email', required=True),
        'role': fields.String(description='Password', required=True),
    })

    @api.doc(body=add_user_fields)
    @jwt_required
    def post(self):
        """
        Create a new user
        """

        id = request.json.get("id")
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
            user = User(id=id, first_name=first_name, last_name=last_name,
                        email=email, password=password_hashed, role=role)
            db.session.add(user)
            db.session.commit()
            ret = {'msg': 'Success'}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Account with that email already exists, please try again with a new email."}), 400)

# Admins can use this route to edit/update a user
@api.route('/update-user/<id>')
class UpdateUser(Resource):

    update_user_fields = api.model('Update User', {
        'first_name': fields.String(description='First Name', required=True),
        'last_name': fields.String(description='Last Name', required=True),
        'email': fields.String(description='Email', required=True),
        'role': fields.String(description='Password', required=True),
    })

    @api.doc(body=update_user_fields)
    @jwt_required
    def put(self, id):
        """
        Update a user
        """

        user = User.query.filter_by(id=id).first()

        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
        email = request.json.get('email')
        role = request.json.get('role')

        temp = User.query.filter_by(email=email).first()

        if temp and temp.id != user.id:
            ret = {
                'msg': 'A user with that email already exists, please use a new email.'}
            return make_response(jsonify(ret), 400)

        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role
            db.session.commit()
            return make_response(jsonify({"msg": "Successfully updated user!"}), 200)
        else:
            ret = {'msg': 'User not found in database'}
            return make_response(jsonify(ret), 400)


# Admins can use this route to delete a user
@api.route('/delete-user/<id>')
@api.doc(params={'id': ''})
class DeleteUser(Resource):

    @jwt_required
    def delete(self, id):
        """
        Delete a user
        """

        user = User.query.filter_by(id=id).first()

        if not user:  # If no user exists with that id, then return error
            ret = {'msg': 'User not found in database'}
            return make_response(jsonify(ret), 400)

        else:
            db.session.delete(user)
            db.session.commit()
            ret = {'msg': 'Successfully deleted user'}
            return make_response(jsonify(ret), 200)


@api.route('/get-users')
class GetUsers(Resource):

    @jwt_required
    def get(self):
        """
        Returns a list of all users
        """

        # get all users from db
        users = User.query.all()

        size = len(users)

        # returns list of users
        return make_response(jsonify(size=size, users=[user.serialize() for user in users]))


@ns_network.route('/all')
class GetNetworks(Resource):
    @jwt_required
    def get(self):
        """
        Returns a list of all Networks
        """

        # get all organizations from db
        networks = Network.query.all()

        size = len(networks)

        # returns list of Organizations as json response
        return make_response(jsonify(size=size, networks=[network.serialize() for network in networks]))


@ns_network.route('/create')
class AddNetwork(Resource):
    add_network_fields = api.model('Add Network', {
        'name': fields.String(descreption='Name', required=True)
    })

    @ns_network.doc(body=add_network_fields)
    @jwt_required
    def post(self):
        """
        Create a new network
        """

        id = request.json.get("id")
        name = request.json.get("name")

        network = Network.query.filter_by(name=name).first()

        if not network:  # If no network exists with that name, then create a new one
            network = Network(id=id, name=name)
            db.session.add(network)
            db.session.commit()
            ret = {'msg': 'Success'}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Network with that name already exists, please try again with a new name."}), 400)


@ns_network.route('/update/<id>')
@ns_network.doc(params={'id': ''})
class UpdateNetwork(Resource):

    update_network_fields = api.model('Update Network', {
        'name': fields.String(description='Name', required=True),
        'description': fields.String(description='Description'),
    })

    @ns_network.doc(body=update_network_fields)
    @jwt_required
    def put(self, id):
        """
        Update a network
        """

        network = Network.query.filter_by(id=id).first()

        name = request.json.get("name")

        temp = Network.query.filter_by(name=name).first()

        if temp and temp.id != network.id:  # if network with that name already exists, return error
            ret = {'msg': 'Network name must be unique, please enter a new name.'}
            return make_response(jsonify(ret), 400)

        description = request.json.get("description")

        if network:
            network.name = name
            network.description = description
            db.session.commit()
            return make_response(jsonify({"msg": "Successfully updated network!"}), 200)
        else:
            ret = {'msg': 'Network not found in database or network '}
            return make_response(jsonify(ret), 400)


@ns_network.route('/delete/<id>')
@ns_network.doc(params={'id': ''})
class DeleteNetwork(Resource):

    @jwt_required
    def delete(self, id):
        """
        Delete a network
        """

        network = Network.query.filter_by(id=id).first()

        if not network:  # If no network exists with that name, then return error
            ret = {'msg': 'Network not found in database'}
            return make_response(jsonify(ret), 400)

        else:
            db.session.delete(network)
            db.session.commit()
            ret = {'msg': 'Successfully deleted network'}
            return make_response(jsonify(ret), 200)


@ns_organization.route('/all/<network_id>')
@ns_organization.doc(params={'network_id': ''})
class GetOrganizations(Resource):
    @jwt_required
    def get(self, network_id):
        """
        Returns a list of all organizations within a network
        """

        # get all organizations from db
        organizations = Organization.query.filter_by(network_id=network_id)

        size = organizations.count()

        # returns list of Organizations as json response
        return make_response(jsonify(size=size, organizations=[organization.serialize() for organization in organizations]))


@ns_organization.route('/create')
class AddOrganization(Resource):
    add_organization_fields = api.model('Add Organization', {
        'name': fields.String(descreption='Name', required=True)
    })

    @ns_organization.doc(body=add_organization_fields)
    @jwt_required
    def post(self):
        """
        Create a new Organization
        """

        id = request.json.get('id')
        name = request.json.get("name")
        network_id = request.json.get('network_id')

        organization = Organization.query.filter_by(
            name=name, network_id=network_id).first()

        if not organization:  # If no organization exists with that name, then create a new one
            organization = Organization(
                id=id, name=name, network_id=network_id)
            db.session.add(organization)
            db.session.commit()
            ret = {'msg': 'Success'}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Organization with that name already exists, please try again with a new name."}), 400)


@ns_organization.route('/update/<id>')
class UpdateOrganization(Resource):
    update_organization_fields = api.model('Update Organization', {
        'name': fields.String(descreption='Name', required=True),
        'description': fields.String(descreption='Description')
    })

    @ns_organization.doc(body=update_organization_fields)
    @jwt_required
    def put(self, id):
        """
        Update an Organization
        """

        organization = Organization.query.filter_by(id=id).first()

        name = request.json.get("name")

        temp = Organization.query.filter_by(name=name).first()

        if temp and temp.id != organization.id:  # if organization with that name already exists, return error
            ret = {'msg': 'Organization name must be unique, please enter a new name.'}
            return make_response(jsonify(ret), 400)

        description = request.json.get("description")

        if organization:
            organization.name = name
            organization.description = description
            db.session.commit()
            return make_response(jsonify({"msg": "Successfully updated organization!"}), 200)
        else:
            ret = {'msg': 'Organization not found in database'}
            return make_response(jsonify(ret), 400)


@ns_organization.route('/delete/<id>')
@ns_organization.doc(params={'id': ''})
class DeleteOrganization(Resource):

    @jwt_required
    def delete(self, id):
        """
        Delete an organization
        """

        organization = Organization.query.filter_by(id=id).first()

        if not organization:  # If no organizstion exists with that name, then return error
            ret = {'msg': 'Organization not found in database'}
            return make_response(jsonify(ret), 400)

        else:
            db.session.delete(organization)
            db.session.commit()
            ret = {'msg': 'Successfully deleted organization'}
            return make_response(jsonify(ret), 200)


@ns_server_group.route('/all/<network_id>/<org_id>')
@ns_server_group.doc(params={'network_id': '', 'org_id': ''})
class GetServerGroupsByOrganization(Resource):

    @jwt_required
    def get(self, network_id, org_id):
        """
        Returns a list of all server groups within an organization
        """

        # get all server groups from db
        server_groups = ServerGroup.query.filter_by(
            network_id=network_id, organization_id=org_id)

        size = server_groups.count()

        # returns list of server groups as json response
        return make_response(jsonify(size=size, server_groups=[server_group.serialize() for server_group in server_groups]))


@ns_server_group.route('/all/<network_id>')
@ns_server_group.doc(params={'network_id': ''})
class GetServerGroupsByNetwork(Resource):

    @jwt_required
    def get(self, network_id):
        """
        Returns a list of all server groups within a network
        """

        # get all server groups from db
        server_groups = ServerGroup.query.filter_by(network_id=network_id)

        size = server_groups.count()

        # returns list of server groups as json response
        return make_response(jsonify(size=size, server_groups=[server_group.serialize() for server_group in server_groups]))


@ns_server_group.route('/create')
class AddServerGroup(Resource):

    add_server_group_fields = api.model('Add Server Group', {
        'name': fields.String(description='Name', required=True),
        'organization': fields.String(description='Organization', required=True),
        'lower_ip_range': fields.String(description='Lower IP Range', required=True),
        'upper_ip_range': fields.String(description='Upper IP Range', required=True),
        'description': fields.String(description='Description', required=True),
        'network_id': fields.String(description='Network Id', required=True)
    })

    @ns_server_group.doc(body=add_server_group_fields)
    @jwt_required
    def post(self):
        """
        Create a new server group
        """

        id = request.json.get("id")
        name = request.json.get("name")
        organization = request.json.get("organization")
        lower_ip_range = request.json.get('lower_ip_range')
        upper_ip_range = request.json.get('upper_ip_range')
        description = request.json.get('description')
        network_id = request.json.get('network_id')

        server_group = ServerGroup.query.filter_by(name=name).first()

        # Check for if the organization given from user exists
        temp = Organization.query.filter_by(name=organization).first()

        if not temp:
            return make_response(jsonify({"msg": "Invalid organization name. Please use an active organization."}), 400)

        if not server_group:  # If no server group exists with that name, then create a new one
            server_group = ServerGroup(id=id, name=name, organization=organization, organization_id=temp.id,
                                       lower_ip_range=lower_ip_range, upper_ip_range=upper_ip_range,
                                       description=description, network_id=network_id)
            db.session.add(server_group)
            db.session.commit()
            ret = {'msg': 'Success'}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Server Group with that name already exists, please try again with a new name."}), 400)


@ns_server_group.route('/update/<id>')
class UpdateServerGroup(Resource):
    update_server_group_fields = api.model('Update Server Group', {
        'name': fields.String(description='Name', required=True),
        'organization': fields.String(description='Organization', required=True),
        'lower_ip_range': fields.String(description='Lower Ip Range', required=True),
        'upper_ip_range': fields.String(description='Lower Ip Range', required=True),
        'description': fields.String(description='Description'),
    })

    @ns_organization.doc(body=update_server_group_fields)
    @jwt_required
    def put(self, id):
        """
        Update a server group
        """

        server_group = ServerGroup.query.filter_by(id=id).first()

        name = request.json.get("name")
        organization = request.json.get("organization")
        lower_ip_range = request.json.get("lower_ip_range")
        upper_ip_range = request.json.get("upper_ip_range")
        description = request.json.get("description")

        temp = ServerGroup.query.filter_by(name=name).first()

        if temp and temp.id != server_group.id:  # if server group with that name already exists, return error
            ret = {'msg': 'Server group name must be unique, please enter a new name.'}
            return make_response(jsonify(ret), 400)

        description = request.json.get("description")

        if server_group:
            server_group.name = name
            server_group.organization = organization
            server_group.lower_ip_range = lower_ip_range
            server_group.upper_ip_range = upper_ip_range
            server_group.description = description
            db.session.commit()
            return make_response(jsonify({"msg": "Successfully updated server group!"}), 200)
        else:
            ret = {'msg': 'Server group not found in database'}
            return make_response(jsonify(ret), 400)


@ns_server_group.route('/delete/<id>')
@ns_server_group.doc(params={'id': ''})
class DeleteServerGroup(Resource):

    @jwt_required
    def delete(self, id):
        """
        Delete a server group
        """

        server_group = ServerGroup.query.filter_by(id=id).first()

        if not server_group:  # If no server group exists with that name, then return error
            ret = {'msg': 'Server group not found in database'}
            return make_response(jsonify(ret), 400)

        else:
            db.session.delete(server_group)
            db.session.commit()
            ret = {'msg': 'Successfully deleted server group'}
            return make_response(jsonify(ret), 200)


@ns_connection.route('/all/<network_id>')
@ns_connection.doc(params={'network_id': ''})
class GetConnections(Resource):

    @jwt_required
    def get(self, network_id):
        """
        Returns a list of all network connections within a network
        """

        # get all network connections from db
        connections = Connection.query.filter_by(network_id=network_id)

        size = connections.count()

        if not connections:  # If no connections exists, then return error
            ret = {'msg': 'No connections found in database'}
            return make_response(jsonify(ret), 400)

        else:
            # returns list of network connections as json response
            return make_response(jsonify(size=size, connections=[connection.serialize() for connection in connections]), 200)


@ns_connection.route('/create')
class AddConnection(Resource):

    add_connection_fields = api.model('Add Connection', {
        'direction': fields.String(description='Description', required=True),
        'organization_A': fields.String(description='Organization A', required=True),
        'organization_B': fields.String(description='Organization B', required=True),
        'server_group_A': fields.String(description='Server Group A', required=True),
        'server_group_B': fields.String(description='Server Group B', required=True),
        'network_id': fields.String(description='Network Id', required=True)
    })

    @ns_server_group.doc(body=add_connection_fields)
    @jwt_required
    def post(self):
        """
        Create a new network connection
        """

        id = request.json.get("id")
        direction = request.json.get("direction")
        organization_A = request.json.get("organization_A")
        organization_B = request.json.get("organization_B")
        server_group_A = request.json.get('server_group_A')
        server_group_B = request.json.get('server_group_B')
        network_id = request.json.get('network_id')

        connection = Connection.query.filter_by(direction=direction, organization_A=organization_A, organization_B=organization_B,
                                                server_group_A=server_group_A, server_group_B=server_group_B, network_id=network_id).first()

        if not connection:  # If that connection doesn't already exists, then we can create a new one
            connection = Connection(id=id, direction=direction, organization_A=organization_A, organization_B=organization_B,
                                    server_group_A=server_group_A, server_group_B=server_group_B, network_id=network_id)
            db.session.add(connection)
            db.session.commit()
            ret = {'msg': 'Success'}
            return make_response(jsonify(ret), 200)

        else:
            return make_response(jsonify({"msg": "Unable to add connection. That connection already exists"}), 400)


@ns_connection.route('/update/<id>')
class UpdateConnection(Resource):
    update_connection_fields = api.model('Update Connection', {
        'name': fields.String(description='Name', required=True),
        'organization': fields.String(description='Organization', required=True),
        'lower_ip_range': fields.String(description='Lower Ip Range', required=True),
        'upper_ip_range': fields.String(description='Lower Ip Range', required=True),
        'description': fields.String(description='Description'),
    })

    @ns_connection.doc(body=update_connection_fields)
    @jwt_required
    def put(self, id):
        """
        Update a network connection
        """

        connection = Connection.query.filter_by(id=id).first()

        direction = request.json.get("direction")
        organization_A = request.json.get("organization_A")
        organization_B = request.json.get("organization_B")
        server_group_A = request.json.get('server_group_A')
        server_group_B = request.json.get('server_group_B')
        network_id = request.json.get('network_id')

        temp = Connection.query.filter_by(direction=direction, organization_A=organization_A, organization_B=organization_B,
                                          server_group_A=server_group_A, server_group_B=server_group_B, network_id=network_id).first()

        if not temp:  # If a connection with these parameters does not already exists, then we can update the connection to the specific parameters

            connection.direction = direction
            connection.organization_A = organization_A
            connection.organization_B = organization_B
            connection.server_group_A = server_group_A
            connection.server_group_B = server_group_B

            db.session.commit()
            return make_response(jsonify({"msg": "Successfully updated network connection!"}), 200)

        else:
            return make_response(jsonify({"msg": "Unable to add connection. That connection already exists"}), 400)


@ns_connection.route('/delete/<id>')
@ns_connection.doc(params={'id': ''})
class DeleteConnection(Resource):

    @jwt_required
    def delete(self, id):
        """
        Delete a network connection
        """

        connection = Connection.query.filter_by(id=id).first()

        if not connection:  # If no connection exists with that id, then return error
            ret = {'msg': 'Network connection not found in database'}
            return make_response(jsonify(ret), 400)

        else:
            db.session.delete(connection)
            db.session.commit()
            ret = {'msg': 'Successfully deleted network connection'}
            return make_response(jsonify(ret), 200)


if __name__ == '__main__':
    app.run()
