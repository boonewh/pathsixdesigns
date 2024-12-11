from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from pathsix import db
from pathsix.models import Projects
from pathsix.pathsix_crm.project.forms import ProjectForm
from flask_security import roles_accepted

project = Blueprint('project', __name__)

@project.route('/projects')
@roles_accepted('admin', 'editor')
def projects():
    """
    View all projects with pagination.
    """
    page = request.args.get('page', 1, type=int)
    projects = Projects.query.paginate(page=page, per_page=25)
    form = ProjectForm()
    return render_template('crm/project/projects.html', projects=projects, form=form, page=page)

@project.route('/projects/new', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Projects(
            project_name=form.project_name.data,  
            project_description=form.project_description.data,  
            project_status=form.project_status.data,  
            project_start=form.project_start.data,  
            project_end=form.project_end.data,  
            project_worth=form.project_worth.data,  
            created_by=current_user.id
        )
        try:
            db.session.add(new_project)
            db.session.commit()
            flash('Project added successfully!', 'success')
            return redirect(url_for('project.projects'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating project: {e}', 'danger')

    return render_template('crm/project/projects.html', form=form, projects=Projects.query.paginate(page=1, per_page=25))

@project.route('/projectreport/<int:id>', methods=['GET'])
@roles_accepted('admin', 'editor')
def report(id):
    """
    Displays detailed information about a project, including associated client or lead.
    """
    project = Projects.query.get_or_404(id)
    form = ProjectForm(obj=project)

    # Related data via Client or Lead
    client = project.client  # Assuming Projects has a relationship with Client
    lead = project.lead  # Assuming Projects has a relationship with Lead

    addresses = client.addresses if client else []
    contacts = client.contacts if client else []
    contact_notes = client.contact_notes if client else []

    return render_template(
        'crm/project/project_report.html',
        project=project,
        form=form,
        addresses=addresses,
        contacts=contacts,
        notes=contact_notes
    )

@project.route('/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'editor')
def edit_project(project_id):
    """
    Edits an existing project.
    """
    project = Projects.query.get_or_404(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        project.project_name = form.name.data
        project.project_description = form.description.data
        project.project_status = form.status.data
        project.project_start = form.start.data
        project.project_end = form.end.data
        project.project_worth = form.worth.data

        try:
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
    project = Projects.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting project: {e}', 'danger')

    return redirect(url_for('project.projects'))
