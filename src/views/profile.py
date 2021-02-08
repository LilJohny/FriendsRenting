from flask import render_template
from flask_login import login_required

from flask import current_app as app


@app.route('/profile')
@login_required
def profile():
    return render_template('hire_friend.html')
