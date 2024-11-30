from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db  
from pathsix.models import Client, Contact, Address, ContactNote 
from pathsix.pathsix_crm.crm_main.forms import ClientForm  
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

    # If validation fails, re-render the same page with form errors
    flash('Failed to add client. Please correct the errors.', 'danger')
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=25)
    return render_template('crm/customer/customers.html', clients=clients, form=form)