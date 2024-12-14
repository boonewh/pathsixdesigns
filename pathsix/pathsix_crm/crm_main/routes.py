from flask import Blueprint, render_template, request, flash, redirect, url_for
from pathsix import db
from pathsix.models import Client, Address, Contact, ContactNote, Account
from flask_login import login_required

crm_main = Blueprint('crm_main', __name__)

@crm_main.route('/crm')
def crm():
    return render_template('crm/crm.html')

@crm_main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '').strip()
    client_results, address_results, contact_results, note_results, account_results = [], [], [], [], []

    if query:
        client_results = Client.query.filter(Client.name.ilike(f'%{query}%')).all()

        address_results = Address.query.filter(
            Address.street.ilike(f'%{query}%') |
            Address.city.ilike(f'%{query}%') |
            Address.state.ilike(f'%{query}%') |
            Address.zip_code.ilike(f'%{query}%')
        ).all()

        contact_results = Contact.query.filter(
            Contact.first_name.ilike(f'%{query}%') |
            Contact.last_name.ilike(f'%{query}%') |
            Contact.email.ilike(f'%{query}%') |
            Contact.phone.ilike(f'%{query}%')
        ).all()

        note_results = ContactNote.query.filter(ContactNote.note.ilike(f'%{query}%')).all()

        account_results = Account.query.filter(
            Account.account_number.ilike(f'%{query}%') |
            Account.account_name.ilike(f'%{query}%')
        ).all()

    return render_template(
        'crm/search_results.html', 
        query=query, 
        client_results=client_results, 
        address_results=address_results, 
        contact_results=contact_results, 
        note_results=note_results, 
        account_results=account_results
    )
