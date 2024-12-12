from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pathsix import db
from pathsix.models import Lead, Client, Contact, Address, ContactNote, Account
from pathsix.pathsix_crm.crm_main.forms import ClientForm

lead = Blueprint('lead', __name__)

@lead.route('/leads')
@login_required
def leads():
    """
    View all leads with pagination.
    """
    page = request.args.get('page', 1, type=int)
    clients = Lead.query.paginate(page=page, per_page=25)
    form = ClientForm()
    return render_template('crm/lead/leads.html', leads=leads, clients=clients, form=form)