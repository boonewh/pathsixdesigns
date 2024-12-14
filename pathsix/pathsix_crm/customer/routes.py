from flask import Blueprint, render_template, request, flash, redirect, url_for
from pathsix import db
from pathsix.models import Client, Address, Contact, ContactNote, Account
from pathsix.pathsix_crm.crm_main.forms import ClientForm
from flask_login import login_required, current_user


customer = Blueprint('customer', __name__)


@customer.route('/customers')
@login_required
def customers():
    """
    View all customers with pagination.
    """
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=25)
    form = ClientForm()
    return render_template('crm/customer/customers.html', clients=clients, form=form)


@customer.route('/customers/new', methods=['GET', 'POST'])
@login_required
def create_client():
    """
    Create a new client, including associated contacts, addresses, and notes.
    """
    form = ClientForm()

    if form.validate_on_submit():
        try:
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
            db.session.flush()  # Get the client_id for related entries

            # Create the Address entry
            if form.street.data and form.city.data and form.state.data and form.zip_code.data:
                address = Address(
                    client_id=new_client.client_id,  # Link to client
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data
                )
                db.session.add(address)

            # Create the Contact entry
            if form.first_name.data and form.last_name.data and form.contact_email.data:
                contact = Contact(
                    client_id=new_client.client_id,  # Link to client
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.contact_email.data,
                    phone=form.contact_phone.data,
                    created_by=current_user.id
                )
                db.session.add(contact)

            # Create the ContactNote entry
            if form.contact_note.data:
                contact_note = ContactNote(
                    client_id=new_client.client_id,  # Link to client
                    note=form.contact_note.data
                )
                db.session.add(contact_note)

            # Commit all changes
            db.session.commit()
            flash('Client added successfully!', 'success')
            return redirect(url_for('customer.customers'))

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            flash(f'An error occurred while adding the client: {str(e)}', 'danger')

    # If validation fails, re-render the same page with errors
    return render_template('crm/customer/customers.html', form=form)


@customer.route('/client_report/<int:client_id>', methods=['GET'])
@login_required
def client_report(client_id):
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
        'crm/customer/client_report.html',
        client=client,
        form=form,
        addresses=client.addresses,
        contacts=client.contacts,
        notes=client.contact_notes
    )


@customer.route('/client_report/<int:client_id>/edit', methods=['POST'])
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
        return redirect(url_for('customer.client_report', client_id=client_id))

    flash('Failed to update client. Please correct the errors.', 'danger')
    return redirect(url_for('customer.client_report', client_id=client_id))


@customer.route('/client_report/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client has been deleted!', 'success')
    return redirect(url_for('customer.customers'))
