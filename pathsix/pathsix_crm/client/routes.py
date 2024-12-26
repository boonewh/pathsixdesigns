from flask import Blueprint, render_template, request, flash, redirect, url_for
from pathsix import db
from pathsix.models import Client, Address, Contact, ContactNote, Account
from pathsix.pathsix_crm.utils.form_generator import create_dynamic_form
from flask_login import login_required, current_user
from datetime import datetime

client = Blueprint('client', __name__)  # Changed from 'customer' to 'client'

@client.route('/clients')  # Changed from '/customers'
@login_required
def clients():  # Changed from customers()
    """
    View all clients with pagination.
    """
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=25)
    form = create_dynamic_form('client') 
    return render_template('crm/client/clients.html', clients=clients, form=form)  


@client.route('/clients/new', methods=['GET', 'POST'])  # Changed from '/customers/new'
@login_required
def create_client():
    """
    Create a new client, including associated account, contacts, addresses, and notes.
    """
    form = create_dynamic_form('client')

    if form.validate_on_submit():
        try:
            # Create the Client entry
            new_client = Client(
                name=request.form.get('name'),
                website=request.form.get('website'),
                pricing_tier=request.form.get('pricing_tier'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                user_id=current_user.id
            )
            db.session.add(new_client)
            db.session.flush()  # Ensures client_id is available

            # Create the Account entry (unique to client functionality)
            account_number = request.form.get('account_number') or f"ACC{new_client.client_id:06}"
            new_account = Account(
                account_number=account_number,
                account_name=request.form.get('name'),
                client_id=new_client.client_id
            )
            db.session.add(new_account)

            # Create Address entry if all fields provided
            street = request.form.get('street')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip_code')
            
            if all([street, city, state, zip_code]):
                address = Address(
                    client_id=new_client.client_id,
                    street=street,
                    city=city,
                    state=state.upper(),
                    zip_code=zip_code
                )
                db.session.add(address)

            # Create Contact entry if required fields provided
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            contact_email = request.form.get('contact_email')
            contact_phone = request.form.get('contact_phone')
            
            if all([first_name, last_name]):
                contact = Contact(
                    client_id=new_client.client_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=contact_email,
                    phone=contact_phone,
                    created_by=current_user.id
                )
                db.session.add(contact)

            db.session.commit()
            flash('Client created successfully!', 'success')
            return redirect(url_for('client.clients'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')

    return render_template('crm/client/clients.html', form=form)


@client.route('/client/<int:client_id>', methods=['GET'])  # Changed URL pattern
@login_required
def client_report(client_id):
    """
    Display detailed information about a client.
    """
    client = Client.query.get_or_404(client_id)
    account = Account.query.filter_by(client_id=client_id).first()
    
    client_form = create_dynamic_form('client')
    contact_form = create_dynamic_form('contact')
    note_form = create_dynamic_form('notes')

    # Pre-populate the client form
    for field in client_form:
        if field.name != 'csrf_token':
            if hasattr(client, field.name):
                field.data = getattr(client, field.name)
            elif field.name == 'account_number' and account:
                field.data = account.account_number

    # Pre-populate address fields if they exist
    address = client.addresses[0] if client.addresses else None
    if address and hasattr(client_form, 'street'):
        client_form.street.data = address.street
        client_form.city.data = address.city
        client_form.state.data = address.state
        client_form.zip_code.data = address.zip_code

    return render_template(
        'crm/client/client_report.html',
        client=client,
        account=account,
        client_form=client_form,
        contact_form=contact_form,
        note_form=note_form,
        contacts=client.contacts,
        notes=client.contact_notes,
        addresses=client.addresses
    )

@client.route('/client/<int:client_id>/edit', methods=['POST'])
@login_required
def edit_client(client_id):
    """
    Edit an existing client's details.
    """
    client = Client.query.get_or_404(client_id)
    
    try:
        # Update main client fields
        client.name = request.form.get('name')
        client.website = request.form.get('website')
        client.pricing_tier = request.form.get('pricing_tier')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')

        # Update or create account
        account = Account.query.filter_by(client_id=client_id).first()
        account_number = request.form.get('account_number')
        
        if account:
            account.account_number = account_number or account.account_number
        else:
            new_account = Account(
                account_number=account_number or f"ACC{client.client_id:06}",
                account_name=client.name,
                client_id=client.client_id
            )
            db.session.add(new_account)

        # Update or create address
        address = Address.query.filter_by(client_id=client_id).first()
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')

        if all([street, city, state, zip_code]):
            if address:
                address.street = street
                address.city = city
                address.state = state.upper()
                address.zip_code = zip_code
            else:
                new_address = Address(
                    client_id=client_id,
                    street=street,
                    city=city,
                    state=state.upper(),
                    zip_code=zip_code
                )
                db.session.add(new_address)

        db.session.commit()
        flash('Client updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('client.client_report', client_id=client_id))


@client.route('/client/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    """
    Delete a client and all associated data.
    """
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully!', 'success')
    return redirect(url_for('client.clients'))

# Add these routes to your client/routes.py

@client.route('/client/<int:client_id>/add_contact', methods=['POST'])
@login_required
def add_contact(client_id):
    """Add a new contact to the client"""
    client = Client.query.get_or_404(client_id)
    
    try:
        new_contact = Contact(
            client_id=client_id,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            created_by=current_user.id
        )
        db.session.add(new_contact)
        db.session.commit()
        flash('Contact added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding contact: {e}', 'danger')
    
    return redirect(url_for('client.client_report', client_id=client_id))

@client.route('/client/<int:client_id>/add_note', methods=['POST'])
@login_required
def add_client_note(client_id):
    """Add a new note to the client"""
    client = Client.query.get_or_404(client_id)
    
    try:
        new_note = ContactNote(
            client_id=client_id,
            note=request.form.get('note'),
            created_at=datetime.utcnow()
        )
        db.session.add(new_note)
        db.session.commit()
        flash('Note added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding note: {e}', 'danger')
    
    return redirect(url_for('client.client_report', client_id=client_id))