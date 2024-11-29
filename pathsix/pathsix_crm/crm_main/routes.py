from flask import Blueprint, render_template, request
from pathsix import db
from pathsix.models import Client, Address, Contact, ContactNote

crm_main = Blueprint('crm_main', __name__)

@crm_main.route('/crm')
def crm():
    return render_template('crm/crm.html') 

@crm_main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '').strip()
    client_results, address_results, contact_results, note_results = [], [], [], []

    if query:
        client_results = Client.query.filter(Client.name.ilike(f'%{query}%')).all()

        # Search Addresses
        address_results = Address.query.filter(
            Address.street.ilike(f'%{query}%') |
            Address.city.ilike(f'%{query}%') |
            Address.state.ilike(f'%{query}%') |
            Address.zip_code.ilike(f'%{query}%')
        ).all()

        # Search Contacts
        contact_results = Contact.query.filter(
            Contact.first_name.ilike(f'%{query}%') |
            Contact.last_name.ilike(f'%{query}%') |
            Contact.email.ilike(f'%{query}%') |
            Contact.phone.ilike(f'%{query}%')
        ).all()

        # Search Contact Notes
        note_results = ContactNote.query.filter(
            ContactNote.note.ilike(f'%{query}%')
        ).all()

    return render_template(
        'crm/search_results.html', 
        query=query, 
        client_results=client_results, 
        address_results=address_results, 
        contact_results=contact_results, 
        note_results=note_results
    )