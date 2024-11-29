from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db  
from pathsix.models import Client, Contact, Address, ContactNote  
from pathsix.pathsix_crm.customer.forms import ClientForm  
from flask import Blueprint

customer = Blueprint('customer', __name__)


@customer.route('/customers')
@login_required
def customers():
    # Fetch all clients and paginate the results
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=25)
    form = ClientForm()
    return render_template('crm/customer/customers.html', clients=clients, form=form)



@customer.route('/customers/new', methods=['GET', 'POST'])
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
        flash('Client added successfully!', 'success')
        return redirect(url_for('customer.customers'))
    flash('Failed to add client. Please correct the errors.', 'danger')
    return redirect(url_for('customer.customers'))

@customer.route('/customers/<int:client_id>', methods=['GET'])
@login_required
def client(client_id):
    # Fetch the client and related data
    client = Client.query.get_or_404(client_id)
    contacts = client.contacts  # Access related contacts
    addresses = client.addresses  # Access related addresses
    notes = client.contact_notes  # Access related notes

    # Initialize the form with client data
    form = ClientForm(obj=client)

    # Populate the form fields for the first address, if it exists
    if client.addresses:  # Check if the client has addresses
        first_address = client.addresses[0]
        form.street.data = first_address.street
        form.city.data = first_address.city
        form.state.data = first_address.state
        form.zip_code.data = first_address.zip_code

    # Populate other fields as needed
    if client.contacts:
        first_contact = client.contacts[0]  # Assuming one primary contact
        form.first_name.data = first_contact.first_name
        form.last_name.data = first_contact.last_name
        form.contact_email.data = first_contact.email
        form.contact_phone.data = first_contact.phone

    if client.contact_notes:
        first_note = client.contact_notes[0]  # Assuming one primary note
        form.contact_note.data = first_note.note

    return render_template(
        'crm/customer/client.html', 
        client=client, 
        contacts=contacts, 
        addresses=client.addresses, 
        notes=notes, 
        form=form
    )

@customer.route('/customers/<int:client_id>/edit', methods=['POST'])
@login_required
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)

    # Initialize the form with submitted data
    form = ClientForm()

    # Validate the form
    if form.validate_on_submit():
        # Update the Client information
        client.name = form.name.data
        client.website = form.website.data
        client.pricing_tier = form.pricing_tier.data
        client.email = form.email.data
        client.phone = form.phone.data

        # Update related entries
        address = Address.query.filter_by(client_id=client_id).first()
        if address:
            address.street = form.street.data
            address.city = form.city.data
            address.state = form.state.data
            address.zip_code = form.zip_code.data

        contact = Contact.query.filter_by(client_id=client_id).first()
        if contact:
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data
            contact.email = form.contact_email.data
            contact.phone = form.contact_phone.data

        contact_note = ContactNote.query.filter_by(client_id=client_id).first()
        if contact_note:
            contact_note.note = form.contact_note.data

        db.session.commit()
        flash('Client information has been updated successfully!', 'success')
        return redirect(url_for('customer.client', client_id=client_id))

    # If validation fails, reload the page with errors
    flash('Failed to update client. Please correct the errors.', 'danger')
    return redirect(url_for('customer.client', client_id=client_id))


@customer.route('/customers/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client has been deleted!', 'success')
    return redirect(url_for('customer.customers'))