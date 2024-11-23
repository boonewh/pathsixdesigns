from flask import Blueprint, render_template
from flask_limiter.errors import RateLimitExceeded

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('crm/errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('crm/errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('crm/errors/500.html'), 500

@errors.app_errorhandler(RateLimitExceeded)
def error_429(error):
    return render_template('crm/errors/429.html'), 429