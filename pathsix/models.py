from datetime import datetime
from pathsix import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login Manager
class User(db.Model, UserMixin):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    clients = db.relationship('Client', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# 1. Client Table
class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(255))
    pricing_tier = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    addresses = db.relationship('Address', backref='client', lazy=True)
    contact_notes = db.relationship('ContactNote', backref='client', lazy=True)
    sales = db.relationship('Sale', backref='client', lazy=True)
    reminders = db.relationship('Reminder', backref='client', lazy=True)
    billing_cycles = db.relationship('BillingCycle', backref='client', lazy=True)
    website_updates = db.relationship('WebsiteUpdate', backref='client', lazy=True)
    mailing_lists = db.relationship('MailingList', backref='client', lazy=True)
    client_websites = db.relationship('ClientWebsite', backref='client', lazy=True)

    def __repr__(self):
        return f"Client('{self.name}', '{self.website}')"

# 2. Address Table
class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    name = db.Column(db.String(100))
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Address('{self.street}', '{self.city}', '{self.state}', '{self.zip_code}')"

# 3. ContactNote Table
class ContactNote(db.Model):
    __tablename__ = 'contact_notes'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactNote('Client ID: {self.client_id}', 'Note: {self.note[:30]}...')"

# 4. Sales Table
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

# 5. BillingCycle Table
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

# 6. Website Updates Table
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

# 7. Mailing List Table
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

# 8. Client Websites Table
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

# 9. Reminders Table
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
