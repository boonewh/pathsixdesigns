from flask import Blueprint, render_template, request, flash, redirect, url_for, flash
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

            flash('Project and Primary Contact created successfully!', 'success')
            return redirect(url_for('project.report', id=new_project.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating project: {e}', 'danger')

    return render_template('crm/project/create_project.html', form=form)

@project.route('/projectreport/<int:id>', methods=['GET'])
@roles_accepted('admin', 'editor')
def report(id):
    """
    Displays detailed information about a project, including primary and additional contacts.
    """
    project = Project.query.get_or_404(id)
    form = ProjectForm()

    # Fetch the primary contact for the project
    primary_contact = (
        Contact.query.filter_by(project_id=project.id, is_primary=True).first() or
        Contact.query.filter_by(project_id=project.id).order_by(Contact.created_at.asc()).first()
    )

    # Fetch additional contacts for the project (excluding the primary)
    additional_contacts = Contact.query.filter_by(project_id=project.id).filter(
        (Contact.is_primary == False) | (Contact.is_primary.is_(None))
    ).all()

    return render_template(
        'crm/project/project_report.html',
        project=project,
        primary_contact=primary_contact,
        additional_contacts=additional_contacts,
        form=form 
    )

@project.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    primary_contact = Contact.query.filter_by(project_id=project.id).first()
    form = ProjectForm(obj=project)

    # Prepopulate contact fields if a primary contact exists
    if primary_contact:
        form.contact_first_name.data = primary_contact.first_name
        form.contact_last_name.data = primary_contact.last_name
        form.contact_email.data = primary_contact.email
        form.contact_phone.data = primary_contact.phone

    if form.validate_on_submit():
        try:
            # Update Project fields
            project.project_name = form.project_name.data
            project.project_description = form.project_description.data
            project.project_status = form.project_status.data
            project.project_start = form.project_start.data
            project.project_end = form.project_end.data
            project.project_worth = form.project_worth.data

            # Update or create Primary Contact
            if primary_contact:
                primary_contact.first_name = form.contact_first_name.data
                primary_contact.last_name = form.contact_last_name.data
                primary_contact.email = form.contact_email.data
                primary_contact.phone = form.contact_phone.data
            else:
                new_contact = Contact(
                    first_name=form.contact_first_name.data,
                    last_name=form.contact_last_name.data,
                    email=form.contact_email.data,
                    phone=form.contact_phone.data,
                    project_id=project.id,
                    created_at=datetime.utcnow(),
                    created_by=current_user.id
                )
                db.session.add(new_contact)

            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('project.report', id=project.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating project: {e}', 'danger')

    return render_template('crm/project/edit_project.html', form=form, project=project)

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
            is_primary=False  # Explicitly set this as not primary
        )
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Additional contact added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding contact: {e}', 'danger')

    return redirect(url_for('project.report', id=project_id))

