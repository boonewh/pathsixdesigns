from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from pathsix import db, login_manager
from sqlalchemy import event
from sqlalchemy.sql import text  # Import for executing raw SQL
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1. Role model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# 2. User Table
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    active = db.Column(db.Boolean, default=True, nullable=False)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    # Tracking fields
    current_login_at = db.Column(db.DateTime, nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(45), nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)
    login_count = db.Column(db.Integer, nullable=True)

    # Specify foreign keys explicitly for the relationship
    clients = db.relationship(
        'Client',
        backref='user',
        lazy=True,
        foreign_keys='Client.user_id'  # Specify the correct foreign key
    )

    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# 3 UserRoles Table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

# 4. Account Table
class Account(db.Model):
    __tablename__ = 'accounts'

    account_number = db.Column(db.String(20), primary_key=True)
    account_name = db.Column(db.String(100), nullable=False, unique=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Account('{self.account_number}', '{self.account_name}')"

@event.listens_for(Account, 'before_insert')
def generate_account_number(mapper, connection, target):
    if not target.account_number:  # If no account number is provided
        # Use raw SQL to get the highest account number
        query = text('SELECT account_number FROM accounts ORDER BY account_number DESC LIMIT 1')
        result = connection.execute(query).scalar()

        if result:
            # Extract the numeric part of the account number
            numeric_part = ''.join(filter(str.isdigit, result))
            new_number = int(numeric_part or 0) + 1
            target.account_number = f"ACC{new_number:06}"  # Example: ACC000001
        else:
            # Default for the first account
            target.account_number = "ACC000001"
        
# 10. Projects Table
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.lead_id'), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=True)
    project_name = db.Column(db.String(255), nullable=False)
    project_description = db.Column(db.Text, nullable=True)
    project_status = db.Column(db.String(20), nullable=False)
    project_start = db.Column(db.DateTime, nullable=True)
    project_end = db.Column(db.DateTime, nullable=True)
    project_worth = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by], backref='projects_created')
    last_updater = db.relationship('User', foreign_keys=[last_updated_by], backref='projects_updated')
    lead = db.relationship('Lead', backref='lead_projects')
    client = db.relationship('Client', backref='projects')
    contacts = db.relationship('Contact', backref='associated_contacts')
    notes = db.relationship('ContactNote', backref='associated_project')


    def __repr__(self):
        return f"Project('{self.project_name}', 'Status: {self.project_status}')"

# 5. Client Table
class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))
    pricing_tier = db.Column(db.String(20))
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    accounts = db.relationship('Account', backref='client', lazy=True, cascade="all, delete-orphan")
    addresses = db.relationship('Address', backref='client', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='company_contacts', lazy=True, cascade="all, delete-orphan")
    contact_notes = db.relationship('ContactNote', backref='client', lazy=True, cascade="all, delete-orphan")
    sales = db.relationship('Sale', backref='client', lazy=True, cascade="all, delete-orphan")
    billing_cycles = db.relationship('BillingCycle', backref='client', lazy=True, cascade="all, delete-orphan")
    website_updates = db.relationship('WebsiteUpdate', backref='client', lazy=True, cascade="all, delete-orphan")
    client_websites = db.relationship('ClientWebsite', backref='client', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('Reminder', backref='client', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Client('{self.name}', '{self.website}')"

# 6. Address Table
class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.lead_id'), nullable=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Address('{self.street}', '{self.city}', '{self.state}', '{self.zip_code}')"



# 7. Contact Table
class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.lead_id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    client = db.relationship('Client', backref='client_contacts')  
    lead = db.relationship('Lead', backref='lead_contacts')  
    project = db.relationship('Project', backref='project_contacts')  



# 8. ContactNote Table
class ContactNote(db.Model):
    __tablename__ = 'contact_notes'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.lead_id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref='notes_for_project')


    
# 9. Leads Table
class Lead(db.Model):
    __tablename__ = 'leads'

    lead_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    lead_description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    addresses = db.relationship('Address', backref='lead', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='associated_lead', lazy=True, cascade="all, delete-orphan")
    projects = db.relationship('Project', backref='parent_lead', lazy=True, cascade="all, delete-orphan")
    contact_notes = db.relationship('ContactNote', backref='lead', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Lead('{self.name}', '{self.email}', '{self.phone}')"

# 11. Sale Table
class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    sale_amount = db.Column(db.Float)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    extras_sold = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Sale('Client ID: {self.client_id}', 'Amount: {self.sale_amount}', 'Date: {self.sale_date}')"

# 12. BillingCycle Table
class BillingCycle(db.Model):
    __tablename__ = 'billing_cycles'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    billing_cycle = db.Column(db.String(10))  # e.g., 'monthly' or 'yearly'
    last_billed = db.Column(db.DateTime)
    next_billing = db.Column(db.DateTime)
    payment_status = db.Column(db.String(10))  # e.g., 'pending', 'paid', 'overdue'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"BillingCycle('Client ID: {self.client_id}', 'Cycle: {self.billing_cycle}', 'Status: {self.payment_status}')"

# 13. WebsiteUpdate Table
class WebsiteUpdate(db.Model):
    __tablename__ = 'website_updates'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    pages_updated = db.Column(db.JSON)
    sections_updated = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"WebsiteUpdate('Client ID: {self.client_id}', 'Date: {self.update_date}')"

# 14. ClientWebsite Table
class ClientWebsite(db.Model):
    __tablename__ = 'client_websites'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    hosting_site = db.Column(db.String(100))
    ssl_status = db.Column(db.String(20))  # e.g., 'active', 'expiring', 'expired'
    renewal_date = db.Column(db.DateTime)
    hosting_cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ClientWebsite('Client ID: {self.client_id}', 'Domain: {self.domain}', 'SSL Status: {self.ssl_status}')"

# 15. Reminder Table
class Reminder(db.Model):
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    reminder_type = db.Column(db.String(50))  # e.g., 'follow-up', 'billing', 'site update'
    reminder_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Reminder('Client ID: {self.client_id}', 'Type: {self.reminder_type}', 'Date: {self.reminder_date}')"
