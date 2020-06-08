from flask import render_template

from app import app


@app.route('/queries')
def queries():
    return render_template('queries.html')
