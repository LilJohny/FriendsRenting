from flask import render_template
from flask_login import login_required, current_user

from ..app import app


@app.route('/actions')
@login_required
def actions():
    if current_user.friend_id is not None:
        return render_template('actions_friends.html')
    elif current_user.client_id is not None:
        return render_template('actions_clients.html')
