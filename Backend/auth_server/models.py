import time
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(55))
    last_name = db.Column(db.String(55))
    password = db.Column(db.String(100))  # hashed password
    email = db.Column(db.String(140), unique=True)
    role = db.Column(db.String(15))

    def __str__(self):
        return self.email

    def get_user_id(self):
        return self.id

    def get_user_role(self):
        return self.role

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def check_password(self, password):
        # checks if hash password in db matches password
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role,
            'id': self.id,
        }

class Network(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Organization(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    network_id = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_network_id(self):
        return self.network_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'network_id': self.network_id
        }


class ServerGroup(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    organization = db.Column(db.String(100))
    category = db.Column(db.String(55))
    lower_ip_range = db.Column(db.String(30))
    upper_ip_range = db.Column(db.String(30))
    description = db.Column(db.String(150))
    network_id = db.Column(db.String(100))
    organization_id = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_organization(self):
        return self.organization

    def get_organization_id(self):
        return self.organization_id

    def get_category(self):
        return self.category

    def get_lower_ip_range(self):
        return self.lower_ip_range

    def get_upper_ip_range(self):
        return self.upper_ip_range

    def get_description(self):
        return self.description

    def get_network_id(self):
        return self.network_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'organization_id': self.organization_id,
            'lower_ip_range': self.lower_ip_range,
            'upper_ip_range': self.upper_ip_range,
            'description': self.description,
            'network_id': self.network_id,
        }

class Connection(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    direction = db.Column(db.String(150))
    organization_A = db.Column(db.String(100))
    organization_B = db.Column(db.String(100))
    server_group_A = db.Column(db.String(100))
    server_group_B = db.Column(db.String(100))
    network_id = db.Column(db.String(100))

    def get_id(self):
        return self.id

    def get_direction(self):
        return self.direction

    def get_organization_A(self):
        return self.organization_A

    def get_organization_B(self):
        return self.organization_B

    def get_server_group_A(self):
        return self.server_group_A

    def get_server_group_B(self):
        return self.server_group_B

    def get_network_id(self):
        return self.network_id

    def serialize(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'organization_A': self.organization_A,
            'organization_B': self.organization_B,
            'server_group_A': self.server_group_A,
            'server_group_B': self.server_group_B,
            'network_id': self.network_id,
        }


class OAuth2Token(db.Model):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()
