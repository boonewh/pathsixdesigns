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
    return render_template('crm/customers.html', clients=clients)


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
        flash('Client and related information added successfully!', 'success')
        return redirect(url_for('crm.customer.customers'))
    return render_template('crm/create_client.html', form=form)

@customer.route('/customers/<int:client_id>', methods=['GET', 'POST'])
@login_required
def client(client_id):
    client = Client.query.get_or_404(client_id)
    contacts = client.contacts # Access the related Contact entries via the relationship
    return render_template('crm/client.html', client=client, contacts=contacts)


@customer.route('/customers/<int:client_id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('crm.customer.client', client_id=client.client_id))

    return render_template('crm/create_client.html', form=form, legend="Edit Client Information")

@customer.route('/customers/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client has been deleted!', 'success')
    return redirect(url_for('crm.customer.customers'))