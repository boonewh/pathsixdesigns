from flask import Blueprint, render_template, request, flash, redirect, url_for
from pathsix import db
from pathsix.models import Client, Address, Contact, ContactNote, Account
from pathsix.pathsix_crm.crm_main.forms import ClientForm
from flask_login import login_required

crm_main = Blueprint('crm_main', __name__)

@crm_main.route('/crm')
def crm():
    return render_template('crm/crm.html')

@crm_main.route('/report/<int:client_id>', methods=['GET'])
@login_required
def report(client_id):
    """
    Displays detailed information about a client, including associated address,
    contact, and notes if available.
    """
    client = Client.query.get_or_404(client_id)
    form = ClientForm(obj=client)

    # Get the first address, contact, and note if they exist
    first_address = client.addresses[0] if client.addresses else None
    first_contact = client.contacts[0] if client.contacts else None
    first_note = client.contact_notes[0] if client.contact_notes else None

    # Populate form fields for the primary address
    if first_address:
        form.street.data = first_address.street
        form.city.data = first_address.city
        form.state.data = first_address.state
        form.zip_code.data = first_address.zip_code

    # Populate form fields for the primary contact
    if first_contact:
        form.first_name.data = first_contact.first_name
        form.last_name.data = first_contact.last_name
        form.contact_email.data = first_contact.email
        form.contact_phone.data = first_contact.phone

    # Populate form field for the primary note
    if first_note:
        form.contact_note.data = first_note.note

    # Pass related data explicitly to the template
    return render_template(
        'crm/report.html',
        client=client,
        form=form,
        addresses=client.addresses,
        contacts=client.contacts,
        notes=client.contact_notes
    )


@crm_main.route('/report/<int:client_id>/edit', methods=['POST'])
@login_required
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = ClientForm()

    if form.validate_on_submit():
        client.name = form.name.data
        client.website = form.website.data
        client.pricing_tier = form.pricing_tier.data
        client.email = form.email.data
        client.phone = form.phone.data

        # Update address
        address = Address.query.filter_by(client_id=client_id).first()
        if address:
            address.street = form.street.data
            address.city = form.city.data
            address.state = form.state.data
            address.zip_code = form.zip_code.data

        # Update contact
        contact = Contact.query.filter_by(client_id=client_id).first()
        if contact:
            contact.first_name = form.first_name.data
            contact.last_name = form.last_name.data
            contact.email = form.contact_email.data
            contact.phone = form.contact_phone.data

        # Update contact note
        contact_note = ContactNote.query.filter_by(client_id=client_id).first()
        if contact_note:
            contact_note.note = form.contact_note.data

        db.session.commit()
        flash('Client information has been updated successfully!', 'success')
        return redirect(url_for('crm_main.report', client_id=client_id))

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
    client_results, address_results, contact_results, note_results, account_results = [], [], [], [], []

    if query:
        client_results = Client.query.filter(Client.name.ilike(f'%{query}%')).all()

        address_results = Address.query.filter(
            Address.street.ilike(f'%{query}%') |
            Address.city.ilike(f'%{query}%') |
            Address.state.ilike(f'%{query}%') |
            Address.zip_code.ilike(f'%{query}%')
        ).all()

        contact_results = Contact.query.filter(
            Contact.first_name.ilike(f'%{query}%') |
            Contact.last_name.ilike(f'%{query}%') |
            Contact.email.ilike(f'%{query}%') |
            Contact.phone.ilike(f'%{query}%')
        ).all()

        note_results = ContactNote.query.filter(ContactNote.note.ilike(f'%{query}%')).all()

        account_results = Account.query.filter(
            Account.account_number.ilike(f'%{query}%') |
            Account.account_name.ilike(f'%{query}%')
        ).all()

    return render_template(
        'crm/search_results.html', 
        query=query, 
        client_results=client_results, 
        address_results=address_results, 
        contact_results=contact_results, 
        note_results=note_results, 
        account_results=account_results
    )
