from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db
from pathsix.models import Client, Contact, Address, ContactNote, Account
from pathsix.pathsix_crm.crm_main.forms import ClientForm

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
