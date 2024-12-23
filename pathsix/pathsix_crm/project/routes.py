import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user
from pathsix import db
from pathsix.models import Project, Contact, ContactNote, Client, Lead
from flask_security import roles_accepted
from datetime import datetime
from pathsix.pathsix_crm.utils.form_generator import create_dynamic_form

# Enable SQLAlchemy query logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

project = Blueprint('project', __name__)

@project.route('/projects', methods=['GET'])
@roles_accepted('admin', 'editor')
def projects():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.created_at.desc()).paginate(page=page, per_page=25)
    
    # Use dynamic form instead of ProjectForm
    form = create_dynamic_form('project')
    
    # Populate select fields
    form.client_id.choices = [('', 'Select Client')] + [(str(c.client_id), c.name) for c in Client.query.all()]
    form.lead_id.choices = [('', 'Select Lead')] + [(str(l.lead_id), l.name) for l in Lead.query.all()]
    
    return render_template('crm/project/projects.html', projects=projects, form=form)


@project.route('/get_companies/<company_type>')
@roles_accepted('admin', 'editor')
def get_companies(company_type):
    """AJAX endpoint to get companies based on type"""
    if company_type == 'client':
        companies = Client.query.all()
        return jsonify([(str(c.client_id), c.name) for c in companies])
    elif company_type == 'lead':
        leads = Lead.query.all()
        return jsonify([(str(l.lead_id), l.name) for l in leads])
    return jsonify([])

# Create Project
@project.route('/create_project', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def create_project():
    form = create_dynamic_form('project')
    
    # Populate select field choices
    form.client_id.choices = [('', 'Select Client')] + [(str(c.client_id), c.name) for c in Client.query.all()]
    form.lead_id.choices = [('', 'Select Lead')] + [(str(l.lead_id), l.name) for l in Lead.query.all()]
    
    if form.validate_on_submit():
        try:
            # Create new project with form data
            new_project = Project()
            for field in form:
                if field.name != 'csrf_token':
                    setattr(new_project, field.name, field.data)
            
            new_project.created_at = datetime.utcnow()
            new_project.created_by = current_user.id
            
            db.session.add(new_project)
            db.session.flush()  # Get the new project ID

            # Create associated contact
            new_contact = Contact(
                project_id=new_project.id,
                created_at=datetime.utcnow(),
                created_by=current_user.id
            )
            db.session.add(new_contact)
            
            db.session.commit()
            flash('Project created successfully!', 'success')
            return redirect(url_for('project.report', id=new_project.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating project: {e}', 'danger')
    
    return render_template('create_project.html', form=form)

# Project Report
@project.route('/project_report/<int:id>', methods=['GET'])
@roles_accepted('admin', 'editor')
def report(id):
    # Get the project and related data
    project = Project.query.get_or_404(id)
    contacts = Contact.query.filter_by(project_id=project.id).all()
    notes = ContactNote.query.filter_by(project_id=project.id).order_by(ContactNote.created_at.desc()).all()
   
    # Create forms using your existing JSON structure
    project_form = create_dynamic_form('project')
    contact_form = create_dynamic_form('contact')
    note_form = create_dynamic_form('notes')
    
    # Populate select fields for project form
    project_form.client_id.choices = [('', 'Select Client')] + [(str(c.client_id), c.name) for c in Client.query.all()]
    project_form.lead_id.choices = [('', 'Select Lead')] + [(str(l.lead_id), l.name) for l in Lead.query.all()]
    
    # Pre-populate project form with existing data
    for field in project_form:
        if field.name != 'csrf_token':
            field.data = getattr(project, field.name, None)
            
    # Pre-populate contact form if contacts exist
    if contacts:
        for field in contact_form:
            if field.name != 'csrf_token':
                field.data = getattr(contacts[0], field.name, None)
   
    return render_template('crm/project/project_report.html',
                         project=project,
                         contacts=contacts,
                         notes=notes,
                         project_form=project_form,
                         contact_form=contact_form,
                         note_form=note_form)

# Edit Project
from datetime import datetime

@project.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = create_dynamic_form('project')
    
    # Set up choices
    form.project_status.choices = [
        ('', 'Select Status'),
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('canceled', 'Canceled')
    ]
    
    form.client_id.choices = [('', 'Select Client')] + [(str(c.client_id), c.name) for c in Client.query.all()]
    form.lead_id.choices = [('', 'Select Lead')] + [(str(l.lead_id), l.name) for l in Lead.query.all()]

    if request.method == 'POST':
        try:
            # Handle dates
            project_start = request.form.get('project_start')
            if project_start:
                project.project_start = datetime.strptime(project_start, '%Y-%m-%d')
            else:
                project.project_start = None

            project_end = request.form.get('project_end')
            if project_end:
                project.project_end = datetime.strptime(project_end, '%Y-%m-%d')
            else:
                project.project_end = None

            # Handle other fields
            project.project_name = request.form.get('project_name')
            project.project_description = request.form.get('project_description')
            project.project_status = request.form.get('project_status')
            
            # Handle numeric fields
            project_worth = request.form.get('project_worth')
            project.project_worth = float(project_worth) if project_worth else None
            
            # Handle IDs
            lead_id = request.form.get('lead_id')
            project.lead_id = int(lead_id) if lead_id else None
            
            client_id = request.form.get('client_id')
            project.client_id = int(client_id) if client_id else None

            project.updated_at = datetime.utcnow()
            project.updated_by = current_user.id

            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('project.report', id=project.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {e}', 'danger')
            print(f"Database error: {str(e)}")

    # Pre-populate form
    for field in form:
        if field.name != 'csrf_token':
            field.data = getattr(project, field.name, None)

    return render_template(
        'crm/project/project_report.html',
        project=project,
        project_form=form,
        contact_form=create_dynamic_form('contact'),
        note_form=create_dynamic_form('notes'),
        contacts=Contact.query.filter_by(project_id=project.id).all(),
        notes=ContactNote.query.filter_by(project_id=project.id).all()
    )


# Delete Project
@project.route('/projects/delete/<int:project_id>', methods=['POST'])
@roles_accepted('admin', 'editor')
def delete_project(project_id):
    """
    Deletes a project by its ID.
    """
    project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting project: {e}', 'danger')

    return redirect(url_for('project.projects'))

# Add Additional Contact
@project.route('/projects/<int:project_id>/add_contact', methods=['POST'])
@roles_accepted('admin', 'editor')
def add_contact(project_id):
    project = Project.query.get_or_404(project_id)
    
    try:
        # Create new contact directly from form data
        new_contact = Contact(
            project_id=project_id,
            first_name=request.form.get('contact_first_name'),
            last_name=request.form.get('contact_last_name'),
            email=request.form.get('contact_email'),
            phone=request.form.get('contact_phone'),
            created_at=datetime.utcnow(),
            created_by=current_user.id
        )
        
        db.session.add(new_contact)
        db.session.commit()
        flash('Additional contact added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding contact: {e}', 'danger')
    
    return redirect(url_for('project.report', id=project_id))

# Edit Project Details
#@project.route('/edit_project_details/<int:project_id>', methods=['POST'])
#@roles_accepted('admin', 'editor')
# def edit_project_details(project_id):
#     project = Project.query.get_or_404(project_id)
#     form = create_dynamic_form('project')
#     if form.validate_on_submit():
#        try:
#            for field in form:
#                if field.name != 'csrf_token':
#                    setattr(project, field.name, field.data)
#            db.session.commit()
#            flash('Project details updated successfully!', 'success')
#        except Exception as e:
#            db.session.rollback()
#            flash(f'Error updating project details: {e}', 'danger')
   
#     return redirect(url_for('project.report', id=project_id))

# Edit Project Contact
@project.route('/edit_project_contact/<int:project_id>', methods=['POST'])
@roles_accepted('admin', 'editor')
def edit_project_contact(project_id):
    project = Project.query.get_or_404(project_id)
    contact = Contact.query.filter_by(project_id=project_id).first()
    form = create_dynamic_form('contact')
    if form.validate_on_submit():
       try:
           if contact:
               for field in form:
                   if field.name != 'csrf_token':
                       setattr(contact, field.name, field.data)
               db.session.commit()
               flash('Contact information updated successfully!', 'success')
           else:
               flash('No contact found for this project.', 'danger')
       except Exception as e:
           db.session.rollback()
           flash(f'Error updating contact: {e}', 'danger')
   
    return redirect(url_for('project.report', id=project_id))

# Add Project Note
@project.route('/add_project_note/<int:project_id>', methods=['POST'])
@roles_accepted('admin', 'editor')
def add_project_note(project_id):
    project = Project.query.get_or_404(project_id)
    form = create_dynamic_form('notes')
    if form.validate_on_submit():
       try:
           new_note = ContactNote(
               project_id=project.id,
               note=form.note.data,
               created_at=datetime.utcnow()
           )
           if project.client_id:
               new_note.client_id = project.client_id
           elif project.lead_id:
               new_note.lead_id = project.lead_id
               
           db.session.add(new_note)
           db.session.commit()
           flash('Note added successfully!', 'success')
       except Exception as e:
           db.session.rollback()
           flash(f'Error adding note: {e}', 'danger')
   
    return redirect(url_for('project.report', id=project_id))