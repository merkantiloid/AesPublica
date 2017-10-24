from app import mainApp
from flask import render_template
from flask_login import login_required

from preston.esi import Preston

@mainApp.route('/characters')
@login_required
def characters():

    preston = Preston(client_id='', client_secret='', client_callback='')
    url = preston.get_authorize_url()

    print(url)

    return render_template('characters.html', title='Characters')