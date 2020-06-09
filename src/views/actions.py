from flask import render_template
from flask_login import login_required

from app import app


@app.route('/actions')
@login_required
def actions():
    return render_template('actions_clients.html')
