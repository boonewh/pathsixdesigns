from flask import Blueprint, render_template, request
from pathsix import db
from pathsix.models import Client, Address, Contact, ContactNote
from pathsix.pathsix_crm.crm_main.forms import ClientForm
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

crm_main = Blueprint('crm_main', __name__)

@crm_main.route('/crm')
def crm():
    return render_template('crm/crm.html') 


@crm_main.route('/report/<int:client_id>', methods=['GET'])
@login_required
def report(client_id):
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
        'crm/report.html', 
        client=client, 
        contacts=contacts, 
        addresses=client.addresses, 
        notes=notes, 
        form=form
    )

@crm_main.route('/report/<int:client_id>/edit', methods=['POST'])
@login_required
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)

    # Initialize the form with submitted data
    form = ClientForm()

    # Validate the form
    if form.validate_on_submit():
        # Update the Client information
        client.account = form.account.data
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
        return redirect(url_for('crm_main.report', client_id=client_id))

    # If validation fails, reload the page with errors
    flash('Failed to update client. Please correct the errors.', 'danger')
    return redirect(url_for('crm_main.report', client_id=client_id))


@crm_main.route('/report/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client has been deleted!', 'success')
    return redirect(url_for('crm_main.crm'))

@crm_main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '').strip()
    client_results, address_results, contact_results, note_results = [], [], [], []

    if query:
        client_results = Client.query.filter(Client.name.ilike(f'%{query}%')).all()

        # Search Addresses
        address_results = Address.query.filter(
            Address.street.ilike(f'%{query}%') |
            Address.city.ilike(f'%{query}%') |
            Address.state.ilike(f'%{query}%') |
            Address.zip_code.ilike(f'%{query}%')
        ).all()

        # Search Contacts
        contact_results = Contact.query.filter(
            Contact.first_name.ilike(f'%{query}%') |
            Contact.last_name.ilike(f'%{query}%') |
            Contact.email.ilike(f'%{query}%') |
            Contact.phone.ilike(f'%{query}%')
        ).all()

        # Search Contact Notes
        note_results = ContactNote.query.filter(
            ContactNote.note.ilike(f'%{query}%')
        ).all()

    return render_template(
        'crm/search_results.html', 
        query=query, 
        client_results=client_results, 
        address_results=address_results, 
        contact_results=contact_results, 
        note_results=note_results
    )