from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db
from pathsix.models import Lead, Contact, Address, ContactNote
from pathsix.pathsix_crm.lead.forms import LeadsForm

lead = Blueprint('lead', __name__)

@lead.route('/leads')
@login_required
def leads():
    """
    View all leads with pagination.
    """
    page = request.args.get('page', 1, type=int)
    leads = Lead.query.paginate(page=page, per_page=25)  # Correctly query leads
    form = LeadsForm()  # Instantiate the form
    return render_template('crm/lead/leads.html', leads=leads, form=form)


@lead.route('/leads/new', methods=['GET', 'POST'])
@login_required
def create_lead():
    """
    Create a new lead, including associated contacts, addresses, and notes.
    """
    form = LeadsForm()
    page = request.args.get('page', 1, type=int)  # Get pagination info
    leads = Lead.query.paginate(page=page, per_page=25)  # Query leads for display

    if form.validate_on_submit():
        try:
            # Create the primary Lead entry
            new_lead = Lead(
                name=form.name.data,
                website=form.website.data,
                email=form.email.data,
                phone=form.phone.data,
                user_id=current_user.id
            )
            db.session.add(new_lead)
            db.session.flush()  # Get the lead_id for related entries

            # Create the Address entry
            if form.street.data and form.city.data and form.state.data and form.zip_code.data:
                address = Address(
                    lead_id=new_lead.lead_id,  # Link to lead
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data
                )
                db.session.add(address)

            # Create the Contact entry
            if form.first_name.data and form.last_name.data and form.contact_email.data:
                contact = Contact(
                    lead_id=new_lead.lead_id,  # Link to lead
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
                    lead_id=new_lead.lead_id,  # Link to lead
                    note=form.contact_note.data
                )
                db.session.add(contact_note)

            # Commit all changes
            db.session.commit()
            flash('Lead added successfully!', 'success')
            return redirect(url_for('lead.leads'))

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            flash(f'An error occurred while adding the lead: {str(e)}', 'danger')

    # If validation fails, re-render the same page with errors
    return render_template('crm/lead/leads.html', form=form, leads=leads)


@lead.route('/report/<int:lead_id>/delete', methods=['POST'])
@login_required
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)  # Fix: Use Lead instead of Client
    db.session.delete(lead)  # Correct variable name
    db.session.commit()
    flash('Lead has been deleted!', 'success')
    return redirect(url_for('lead.leads'))


@lead.route('/leads_report/<int:lead_id>', methods=['GET'])
@login_required
def lead_report(lead_id):
    """
    Displays detailed information about a clead, including associated address,
    contact, and notes if available.
    """
    lead = Lead.query.get_or_404(lead_id)
    form = LeadsForm(obj=lead)

    # Get the first address, contact, and note if they exist
    first_address = lead.addresses[0] if lead.addresses else None
    first_contact = lead.contacts[0] if lead.contacts else None
    first_note = lead.contact_notes[0] if lead.contact_notes else None

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
        'crm/lead/leads_report.html',
        lead=lead,
        form=form,
        addresses=lead.addresses,
        contacts=lead.contacts,
        notes=lead.contact_notes
    )

@lead.route('/leads/<int:lead_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lead(lead_id):
    """
    Edit an existing lead's details.
    """
    lead = Lead.query.get_or_404(lead_id)
    form = LeadsForm(obj=lead)

    if form.validate_on_submit():
        try:
            # Update the lead fields
            lead.name = form.name.data
            lead.website = form.website.data
            lead.email = form.email.data
            lead.phone = form.phone.data

            # Update the address
            address = Address.query.filter_by(lead_id=lead_id).first()
            if address:
                address.street = form.street.data
                address.city = form.city.data
                address.state = form.state.data
                address.zip_code = form.zip_code.data

            # Update the contact
            contact = Contact.query.filter_by(lead_id=lead_id).first()
            if contact:
                contact.first_name = form.first_name.data
                contact.last_name = form.last_name.data
                contact.email = form.contact_email.data
                contact.phone = form.contact_phone.data

            # Update the contact note
            contact_note = ContactNote.query.filter_by(lead_id=lead_id).first()
            if contact_note:
                contact_note.note = form.contact_note.data

            db.session.commit()
            flash('Lead has been updated successfully!', 'success')
            return redirect(url_for('lead.lead_report', lead_id=lead_id))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the lead: {str(e)}', 'danger')

    return render_template('crm/lead/leads_report.html', form=form, lead=lead)
