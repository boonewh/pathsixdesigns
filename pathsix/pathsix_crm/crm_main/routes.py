from flask import Blueprint, render_template

crm_main = Blueprint('crm_main', __name__)

@crm_main.route('/crm')
def crm():
    return render_template('crm/crm.html') 