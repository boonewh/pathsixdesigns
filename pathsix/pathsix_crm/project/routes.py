from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from pathsix import db
from pathsix.models import Project, Contact
from pathsix.pathsix_crm.project.forms import ProjectForm
from flask_security import roles_accepted
from datetime import datetime

project = Blueprint('project', __name__)

@project.route('/projects')
@roles_accepted('admin', 'editor')
def projects():
    """
    View all projects with pagination.
    """
    page = request.args.get('page', 1, type=int)
    projects = Project.query.paginate(page=page, per_page=25)
    form = ProjectForm()
    return render_template('crm/project/projects.html', projects=projects, form=form, page=page)

# Create Project
@project.route('/create_project', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        try:
            # Create the Project
            new_project = Project(
                project_name=form.project_name.data,
                project_description=form.project_description.data,
                project_status=form.project_status.data,
                project_start=form.project_start.data,
                project_end=form.project_end.data,
                project_worth=form.project_worth.data,
                created_at=datetime.utcnow(),
                created_by=current_user.id
            )
            db.session.add(new_project)
            db.session.flush()  # Get project ID without committing

            # Create the Primary Contact
            new_contact = Contact(
                first_name=form.contact_first_name.data,
                last_name=form.contact_last_name.data,
                email=form.contact_email.data,
                phone=form.contact_phone.data,
                project_id=new_project.id,  # Link to the project
                created_at=datetime.utcnow(),
                created_by=current_user.id
            )
            db.session.add(new_contact)

            # Commit both to the database
            db.session.commit()

            flash('Project Contact created successfully!', 'success')
            return redirect(url_for('project.report', id=new_project.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating project: {e}', 'danger')

    return render_template('crm/project/client_report.html', form=form)

# Project Report
@project.route('/projectreport/<int:id>', methods=['GET'])
@roles_accepted('admin', 'editor')
def report(id):
    project = Project.query.get_or_404(id)
    contacts = Contact.query.filter_by(project_id=project.id).order_by(Contact.created_at.asc()).all()
    notes = project.notes
    
    # Create form and populate with project data
    form = ProjectForm(obj=project)
    
    # If there's a contact, populate contact fields
    if contacts and contacts[0]:  # Get the first contact if it exists
        contact = contacts[0]
        form.contact_first_name.data = contact.first_name
        form.contact_last_name.data = contact.last_name
        form.contact_email.data = contact.email
        form.contact_phone.data = contact.phone

    return render_template(
        'crm/project/project_report.html',
        project=project,
        contacts=contacts,
        notes=notes,
        form=form
    )

# Edit Project
@project.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    contacts = Contact.query.filter_by(project_id=project_id).all()
    contact = contacts[0] if contacts else None

    print(f"Initial contact data: {contact.__dict__ if contact else 'No contact'}")  # Debug

    form = ProjectForm(obj=project)
    
    if request.method == 'POST':
        print(f"Form data received: {request.form}")  # Debug

    if form.validate_on_submit():
        try:
            print("Form validated successfully")  # Debug
            
            # Update project fields
            project.project_name = form.project_name.data
            project.project_description = form.project_description.data
            project.project_status = form.project_status.data
            project.project_start = form.project_start.data
            project.project_end = form.project_end.data
            project.project_worth = form.project_worth.data

            print(f"Project updated with: {project.__dict__}")  # Debug

            # Handle contact update
            if contact:
                print(f"Contact before update: {contact.__dict__}")  # Debug
                contact.first_name = form.contact_first_name.data
                contact.last_name = form.contact_last_name.data
                contact.email = form.contact_email.data
                contact.phone = form.contact_phone.data
                contact.updated_at = datetime.utcnow()
                print(f"Contact after update: {contact.__dict__}")  # Debug
            else:
                print("Creating new contact")  # Debug
                new_contact = Contact(
                    project_id=project.id,
                    first_name=form.contact_first_name.data,
                    last_name=form.contact_last_name.data,
                    email=form.contact_email.data,
                    phone=form.contact_phone.data,
                    created_by=current_user.id
                )
                db.session.add(new_contact)
            
            db.session.commit()
            print("Database committed successfully")  # Debug
            
            # Verify the changes
            updated_contact = Contact.query.filter_by(project_id=project_id).first()
            print(f"Contact after commit: {updated_contact.__dict__}")  # Debug
            
            flash('Project and contact information updated successfully!', 'success')
            return redirect(url_for('project.report', id=project.id))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {str(e)}")  # Debug
            flash(f'Error updating project: {e}', 'danger')

    return render_template(
        'crm/project/edit_project.html',
        form=form,
        project=project
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
    form = ProjectForm()

    if form.validate_on_submit():
        new_contact = Contact(
            first_name=form.contact_first_name.data,
            last_name=form.contact_last_name.data,
            email=form.contact_email.data,
            phone=form.contact_phone.data,
            project_id=project.id,
            created_at=datetime.utcnow(),
            created_by=current_user.id,
        )
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Additional contact added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding contact: {e}', 'danger')

    return redirect(url_for('project.report', id=project_id))