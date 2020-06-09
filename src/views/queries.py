from flask import render_template
from flask_login import login_required

from app import app


@app.route('/queries')
@login_required
def queries():
    return render_template('queries.html')
