from flask import render_template

from app import app


@app.route('/actions')
def actions():
    return render_template('actions_clients.html')
