from flask import Blueprint, render_template, request
from pathsix.models import Client
from pathsix.pathsix_crm.crm_main.forms import ClientForm
from flask_security import roles_accepted

project = Blueprint('project', __name__)

@project.route('/projects')
@roles_accepted('admin', 'editor')
def customers():
    # Fetch all clients and paginate the results
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=25)
    form = ClientForm()
    return render_template('crm/project/projects.html', clients=clients, form=form)