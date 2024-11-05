from flask import render_template, request, redirect, url_for, flash
from pathsix import app, mail, bcrypt, db
from pathsix.forms import ContactForm, RegistrationForm, LoginForm, UpdateAccountForm, ClientForm
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
    # Query all clients and eager load related addresses
    clients = Client.query.all()
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
    return render_template('crm/client.html', client=client)