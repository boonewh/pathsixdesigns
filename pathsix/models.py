from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from pathsix import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1. User Table
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    clients = db.relationship('Client', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], salt='email-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], salt='email-reset')
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 2. Client Table
class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))
    pricing_tier = db.Column(db.String(20))
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships with cascading delete
    addresses = db.relationship('Address', backref='client', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='client', lazy=True, cascade="all, delete-orphan")
    contact_notes = db.relationship('ContactNote', backref='client', lazy=True, cascade="all, delete-orphan")
    sales = db.relationship('Sale', backref='client', lazy=True, cascade="all, delete-orphan")
    billing_cycles = db.relationship('BillingCycle', backref='client', lazy=True, cascade="all, delete-orphan")
    website_updates = db.relationship('WebsiteUpdate', backref='client', lazy=True, cascade="all, delete-orphan")
    mailing_lists = db.relationship('MailingList', backref='client', lazy=True, cascade="all, delete-orphan")
    client_websites = db.relationship('ClientWebsite', backref='client', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('Reminder', backref='client', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Client('{self.name}', '{self.website}')"


# 3. Address Table
class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Address('{self.street}', '{self.city}', '{self.state}', '{self.zip_code}')"

# 4. Contact Table
class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Contact('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone}')"

# 5. ContactNote Table
class ContactNote(db.Model):
    __tablename__ = 'contact_notes'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactNote('Client ID: {self.client_id}', 'Note: {self.note[:30]}...')"

# 6. Sale Table
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

# 7. BillingCycle Table
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

# 8. WebsiteUpdate Table
class WebsiteUpdate(db.Model):
    __tablename__ = 'website_updates'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    pages_updated = db.Column(db.JSON)
    sections_updated = db.Column(db.JSON)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"WebsiteUpdate('Client ID: {self.client_id}', 'Date: {self.update_date}')"

# 9. MailingList Table
class MailingList(db.Model):
    __tablename__ = 'mailing_list'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    address = db.Column(db.String(255))
    postcard_sent = db.Column(db.Boolean, default=False)
    date_sent = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"MailingList('Client ID: {self.client_id}', 'Address: {self.address}', 'Postcard Sent: {self.postcard_sent}')"

# 10. ClientWebsite Table
class ClientWebsite(db.Model):
    __tablename__ = 'client_websites'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    hosting_site = db.Column(db.String(100))
    ssl_status = db.Column(db.String(20))  # e.g., 'active', 'expiring', 'expired'
    renewal_date = db.Column(db.DateTime)
    hosting_cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ClientWebsite('Client ID: {self.client_id}', 'Domain: {self.domain}', 'SSL Status: {self.ssl_status}')"

# 11. Reminder Table
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
