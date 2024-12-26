from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db
from pathsix.models import Project, Lead, Contact, Address, ContactNote
from pathsix.pathsix_crm.utils.form_generator import create_dynamic_form
from datetime import datetime

lead = Blueprint('lead', __name__)

@lead.route('/leads')
@login_required
def leads():
    """
    View all leads with pagination and prepare form for creating new leads.
    """
    page = request.args.get('page', 1, type=int)
    leads = Lead.query.paginate(page=page, per_page=25)
    form = create_dynamic_form('lead')
    return render_template('crm/lead/leads.html', leads=leads, form=form)

# Create Leads
@lead.route('/leads/new', methods=['GET', 'POST'])
@login_required
def create_lead():
    """
    Create a new lead, including associated contacts, addresses, and notes.
    """
    form = create_dynamic_form('lead')

    if request.method == 'POST':
        try:
            # Create the Lead entry
            new_lead = Lead(
                name=request.form.get('name'),
                website=request.form.get('website'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                lead_description=request.form.get('lead_description'),
                user_id=current_user.id
            )
            db.session.add(new_lead)
            db.session.flush()  # Ensure lead_id is generated

            # Create Address entry if all fields are provided
            street = request.form.get('street')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip_code')
            
            if all([street, city, state, zip_code]):
                address = Address(
                    lead_id=new_lead.lead_id,
                    street=street,
                    city=city,
                    state=state.upper(),
                    zip_code=zip_code
                )
                db.session.add(address)

            # Create Contact entry if required fields are provided
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            contact_email = request.form.get('contact_email')
            contact_phone = request.form.get('contact_phone')
            
            if all([first_name, last_name]):
                contact = Contact(
                    lead_id=new_lead.lead_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=contact_email,
                    phone=contact_phone,
                    created_by=current_user.id
                )
                db.session.add(contact)

            # Create ContactNote entry if provided
            note = request.form.get('contact_note')
            if note:
                contact_note = ContactNote(
                    lead_id=new_lead.lead_id,
                    note=note
                )
                db.session.add(contact_note)

            db.session.commit()
            flash('Lead created successfully!', 'success')
            return redirect(url_for('lead.leads'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while adding the lead: {str(e)}', 'danger')

    return render_template('crm/lead/leads.html', form=form)

# Lead Report
@lead.route('/leads_report/<int:lead_id>', methods=['GET'])
@login_required
def lead_report(lead_id):
    """
    Display detailed information about a lead.
    """
    lead = Lead.query.get_or_404(lead_id)
    lead_form = create_dynamic_form('lead')
    contact_form = create_dynamic_form('contact')
    note_form = create_dynamic_form('notes')

    # Get addresses explicitly
    addresses = Address.query.filter_by(lead_id=lead_id).all()
    
    # Pre-populate the lead form
    for field in lead_form:
        if field.name != 'csrf_token':
            if hasattr(lead, field.name):
                field.data = getattr(lead, field.name)

    return render_template(
        'crm/lead/leads_report.html',
        lead=lead,
        lead_form=lead_form,
        contact_form=contact_form,
        note_form=note_form,
        contacts=lead.contacts,
        notes=lead.contact_notes,
        addresses=addresses  # Add this explicitly
    )

# Edit Leads
@lead.route('/leads/<int:lead_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lead(lead_id):
    """
    Edit an existing lead's details.
    """
    lead = Lead.query.get_or_404(lead_id)
    form = create_dynamic_form('lead')
    
    if request.method == 'POST':
        try:
            # Update Lead fields
            lead.name = request.form.get('name')
            lead.website = request.form.get('website')
            lead.email = request.form.get('email')
            lead.phone = request.form.get('phone')
            lead.lead_description = request.form.get('lead_description')
            lead.last_updated_by = current_user.id
            lead.updated_at = datetime.utcnow()

            # Update or create address
            address = Address.query.filter_by(lead_id=lead_id).first()
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
                        lead_id=lead_id,
                        street=street,
                        city=city,
                        state=state.upper(),
                        zip_code=zip_code
                    )
                    db.session.add(new_address)

            db.session.commit()
            flash('Lead updated successfully!', 'success')
            return redirect(url_for('lead.lead_report', lead_id=lead_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating the lead: {str(e)}', 'danger')
    
    # Pre-populate form with existing data
    for field in form:
        if field.name != 'csrf_token':
            if hasattr(lead, field.name):
                field.data = getattr(lead, field.name)

    # Pre-populate address fields if they exist
    address = Address.query.filter_by(lead_id=lead_id).first()
    if address:
        if hasattr(form, 'street'):
            form.street.data = address.street
        if hasattr(form, 'city'):
            form.city.data = address.city
        if hasattr(form, 'state'):
            form.state.data = address.state
        if hasattr(form, 'zip_code'):
            form.zip_code.data = address.zip_code

    contacts = Contact.query.filter_by(lead_id=lead_id).all()
    notes = ContactNote.query.filter_by(lead_id=lead_id).order_by(ContactNote.created_at.desc()).all()

    return render_template(
        'crm/lead/leads_report.html',
        lead=lead,
        lead_form=form,  # Added this
        contact_form=create_dynamic_form('contact'),  # And this
        note_form=create_dynamic_form('notes'),  # And this
        contacts=contacts,
        notes=notes,
        addresses=lead.addresses
    )

@lead.route('/leads/<int:lead_id>/add_contact', methods=['POST'])
@login_required
def add_contact(lead_id):
    """Add a new contact to the lead"""
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        new_contact = Contact(
            lead_id=lead_id,
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
    
    return redirect(url_for('lead.lead_report', lead_id=lead_id))

@lead.route('/leads/<int:lead_id>/add_note', methods=['POST'])
@login_required
def add_lead_note(lead_id):
    """Add a new note to the lead"""
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        new_note = ContactNote(
            lead_id=lead_id,
            note=request.form.get('note'),
            created_at=datetime.utcnow()
        )
        db.session.add(new_note)
        db.session.commit()
        flash('Note added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding note: {e}', 'danger')
    
    return redirect(url_for('lead.lead_report', lead_id=lead_id))

# Delete Leads
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