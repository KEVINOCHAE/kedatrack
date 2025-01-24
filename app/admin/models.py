from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum, func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from enum import Enum


# ---------------------------------------
# contact model
# ---------------------------------------

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage {self.subject} from {self.name}>"


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)  # Role name
    description = db.Column(db.String(255), nullable=True)  # Optional description for the role

    # Relationship to Users
    users = db.relationship('User', back_populates='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

    @staticmethod
    def get_by_name(name):
        """Fetch a role by name."""
        return Role.query.filter_by(name=name).first()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Role
    role = db.relationship('Role', back_populates='users')

    # Methods
    def set_password(self, password):
        """Generate a hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        """Check if the user has a specific role."""
        return self.role and self.role.name == role_name

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def get_by_email(email):
        """Fetch a user by email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        """Fetch a user by username."""
        return User.query.filter_by(username=username).first()


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.String(255), nullable=False)
    service_title = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    subscribe_to_newsletter = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ServiceRequest {self.name}>'
    

class NewsletterSubscriber(db.Model):
    __tablename__ = 'newsletter_subscribers'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Subscriber {self.email}>'


class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.Text, nullable=False)  # Comma-separated list of email addresses
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailLog {self.subject} sent to {self.recipients}>"