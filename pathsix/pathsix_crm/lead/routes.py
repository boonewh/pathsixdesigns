from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db
from pathsix.models import Project, Lead, Contact, Address, ContactNote
from pathsix.pathsix_crm.lead.forms import LeadsForm

lead = Blueprint('lead', __name__)

@lead.route('/leads')
@login_required
def leads():
    """
    View all leads with pagination.
    """
    page = request.args.get('page', 1, type=int)
    leads = Lead.query.paginate(page=page, per_page=25)
    form = LeadsForm()
    return render_template('crm/lead/leads.html', leads=leads, form=form)


@lead.route('/leads/new', methods=['GET', 'POST'])
@login_required
def create_lead():
    """
    Create a new lead, including associated contacts, addresses, and notes.
    """
    form = LeadsForm()

    if form.validate_on_submit():
        try:
            # Create the Lead entry
            new_lead = Lead(
                name=form.name.data,
                website=form.website.data,
                email=form.email.data,
                phone=form.phone.data,
                lead_description=form.lead_description.data,
                user_id=current_user.id
            )
            db.session.add(new_lead)
            db.session.flush()  # Ensure lead_id is generated

            # Create Address entry
            if all([form.street.data, form.city.data, form.state.data, form.zip_code.data]):
                address = Address(
                    lead_id=new_lead.lead_id,
                    street=form.street.data,
                    city=form.city.data,
                    state=form.state.data,
                    zip_code=form.zip_code.data
                )
                db.session.add(address)

            # Create Contact entry
            if all([form.first_name.data, form.last_name.data, form.contact_email.data]):
                contact = Contact(
                    lead_id=new_lead.lead_id,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.contact_email.data,
                    phone=form.contact_phone.data,
                    created_by=current_user.id
                )
                db.session.add(contact)

            # Create ContactNote entry
            if form.contact_note.data:
                contact_note = ContactNote(
                    lead_id=new_lead.lead_id,
                    note=form.contact_note.data
                )
                db.session.add(contact_note)

            db.session.commit()
            flash('Lead created successfully!', 'success')
            return redirect(url_for('lead.leads'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while adding the lead: {str(e)}', 'danger')

    return render_template('crm/lead/leads.html', form=form)


@lead.route('/leads_report/<int:lead_id>', methods=['GET'])
@login_required
def lead_report(lead_id):
    """
    Display detailed information about a lead, including associated address,
    contact, and notes.
    """
    lead = Lead.query.get_or_404(lead_id)
    form = LeadsForm(obj=lead)

    # Get the first address, contact, and note if they exist
    address = lead.addresses[0] if lead.addresses else None
    contact = lead.contacts[0] if lead.contacts else None
    note = lead.contact_notes[0] if lead.contact_notes else None

    # Populate Address fields
    if address:
        form.street.data = address.street
        form.city.data = address.city
        form.state.data = address.state
        form.zip_code.data = address.zip_code

    # Populate Contact fields
    if contact:
        form.first_name.data = contact.first_name
        form.last_name.data = contact.last_name
        form.contact_email.data = contact.email
        form.contact_phone.data = contact.phone

    # Populate ContactNote field
    if note:
        form.contact_note.data = note.note

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
            # Update Lead fields
            lead.name = form.name.data
            lead.website = form.website.data
            lead.email = form.email.data
            lead.phone = form.phone.data
            lead.lead_description = form.lead_description.data

            # Update Address
            address = Address.query.filter_by(lead_id=lead_id).first()
            if address:
                address.street = form.street.data
                address.city = form.city.data
                address.state = form.state.data
                address.zip_code = form.zip_code.data
            else:
                if all([form.street.data, form.city.data, form.state.data, form.zip_code.data]):
                    new_address = Address(
                        lead_id=lead_id,
                        street=form.street.data,
                        city=form.city.data,
                        state=form.state.data,
                        zip_code=form.zip_code.data
                    )
                    db.session.add(new_address)

            # Update Contact
            contact = Contact.query.filter_by(lead_id=lead_id).first()
            if contact:
                contact.first_name = form.first_name.data
                contact.last_name = form.last_name.data
                contact.email = form.contact_email.data
                contact.phone = form.contact_phone.data
            else:
                if all([form.first_name.data, form.last_name.data, form.contact_email.data]):
                    new_contact = Contact(
                        lead_id=lead_id,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.contact_email.data,
                        phone=form.contact_phone.data,
                        created_by=current_user.id
                    )
                    db.session.add(new_contact)

            # Update ContactNote
            contact_note = ContactNote.query.filter_by(lead_id=lead_id).first()
            if contact_note:
                contact_note.note = form.contact_note.data
            else:
                if form.contact_note.data:
                    new_contact_note = ContactNote(
                        lead_id=lead_id,
                        note=form.contact_note.data
                    )
                    db.session.add(new_contact_note)

            db.session.commit()
            flash('Lead updated successfully!', 'success')
            return redirect(url_for('lead.lead_report', lead_id=lead_id))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the lead: {str(e)}', 'danger')

    return render_template('crm/lead/leads_report.html', form=form, lead=lead)


@lead.route('/leads/<int:lead_id>/delete', methods=['POST'])
@login_required
def delete_lead(lead_id):
    """
    Delete a lead and all associated data.
    """
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    flash('Lead deleted successfully!', 'success')
    return redirect(url_for('lead.leads'))
