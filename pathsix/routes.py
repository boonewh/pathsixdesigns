import urllib.parse
from flask import render_template, request, redirect, url_for, flash
from pathsix import app, mail, bcrypt, db
from pathsix.forms import ContactForm, RegistrationForm, LoginForm, UpdateAccountForm, ClientForm, RequestResetForm, ResetPasswordForm
from flask_mail import Message
from pathsix.models import User, Client, Address, Contact, ContactNote, Sale, BillingCycle, WebsiteUpdate, MailingList, ClientWebsite, Reminder
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            for field_errors in form.errors.values():
                for error in field_errors:
                    flash(error, 'error')
            return redirect(url_for('contact'))
        else:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']]
            )
            msg.body = f"""
            This message was sent from the PathSix Web Design contact form.

            From: {form.name.data} <{form.email.data}>
            Message:
            {form.message.data}
            """
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/crm')
def crm():
    return render_template('crm/crm.html') 

@app.route('/customers')
@login_required
def customers():
    # Fetch all clients and paginate the results
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=25)
    return render_template('crm/customers.html', clients=clients)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('crm'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('crm/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('crm'))   
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('crm/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('crm'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('crm/account.html', form=form)

@app.route('/customers/new', methods=['GET', 'POST'])
@login_required
def create_client():
    form = ClientForm()
    if request.method == 'GET':
        # Prefill the website field with "https://"
        form.website.data = 'https://'

    if form.validate_on_submit():
        # Create the primary Client entry
        new_client = Client(
            name=form.name.data,
            website=form.website.data,
            pricing_tier=form.pricing_tier.data,
            email=form.email.data,
            phone=form.phone.data,
            user_id=current_user.id
        )
        db.session.add(new_client)
        db.session.flush()  # Temporarily writes new_client to get its client_id

        # Create the Contact entry
        contact = Contact(
            client_id=new_client.client_id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.contact_email.data,
            phone=form.contact_phone.data
        )
        db.session.add(contact)

        # Create related entries
        address = Address(
            client_id=new_client.client_id,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data
        )
        db.session.add(address)

        contact_note = ContactNote(
            client_id=new_client.client_id,
            note=form.contact_note.data
        )
        db.session.add(contact_note)

        # Commit all changes as a single transaction
        db.session.commit()
        flash('Client and related information added successfully!', 'success')
        return redirect(url_for('customers'))
    return render_template('crm/create_client.html', form=form)

@app.route('/customers/<int:client_id>', methods=['GET', 'POST'])
@login_required
def client(client_id):
    client = Client.query.get_or_404(client_id)
    contacts = client.contacts # Access the related Contact entries via the relationship
    return render_template('crm/client.html', client=client, contacts=contacts)


@app.route('/customers/<int:client_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    # Retrieve the existing client and related entries
    client = Client.query.get_or_404(client_id)
    
    # Initialize the form with data from the Client table
    form = ClientForm(obj=client)

    # Fetch related entries if they exist
    address = Address.query.filter_by(client_id=client_id).first()
    contact = Contact.query.filter_by(client_id=client_id).first()
    contact_note = ContactNote.query.filter_by(client_id=client_id).first()

    if request.method == 'GET':
        # Populate the form fields for Address if it exists
        if address:
            form.street.data = address.street
            form.city.data = address.city
            form.state.data = address.state
            form.zip_code.data = address.zip_code

        # Populate the form fields for Contact if it exists
        if contact:
            form.first_name.data = contact.first_name
            form.last_name.data = contact.last_name
            form.contact_email.data = contact.email
            form.contact_phone.data = contact.phone

        # Populate the form field for ContactNote if it exists
        if contact_note:
            form.contact_note.data = contact_note.note

    if form.validate_on_submit():
        # Update the Client information
        client.name = form.name.data
        client.website = form.website.data
        client.pricing_tier = form.pricing_tier.data
        client.email = form.email.data
        client.phone = form.phone.data

        # Update Address information
        if address:
            address.street = form.street.data
            address.city = form.city.data
            address.state = form.state.data
            address.zip_code = form.zip_code.data

        # Update Contact information
        if contact:
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data
            contact.email = form.contact_email.data
            contact.phone = form.contact_phone.data

        # Update ContactNote if it exists
        if contact_note:
            contact_note.note = form.contact_note.data

        db.session.commit()
        flash("Client information has been updated!", "success")
        return redirect(url_for('client', client_id=client.client_id))

    return render_template('crm/create_client.html', form=form, legend="Edit Client Information")

@app.route('/customers/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client has been deleted!', 'success')
    return redirect(url_for('customers'))

def send_reset_email(user):
    token = user.get_reset_token()
    encoded_token = urllib.parse.quote(token)  # URL-encode the token
    msg = Message('Password Reset Request', 
                  sender='noreply@pathsixdesigns.com', 
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg) 

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('crm'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('crm/reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('crm'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('crm/reset_token.html', form=form)