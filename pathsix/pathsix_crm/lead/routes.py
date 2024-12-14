from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db
from pathsix.models import Lead, Client, Contact, Address, ContactNote, Account
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