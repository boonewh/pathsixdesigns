from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user  # Import current_user
from pathsix import db
from pathsix.models import Projects, Account
from pathsix.pathsix_crm.project.forms import ProjectForm
from flask_security import roles_accepted
import logging

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
            project_name=form.name.data,
            project_description=form.description.data,
            project_status=form.status.data,
            project_start=form.start.data,
            project_end=form.end.data,
            project_worth=form.worth.data,
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
