from app.errors import bp
from flask import render_template, redirect, url_for

@bp.app_errorhandler(404)
def error(e):
    return render_template('errors/error.html')