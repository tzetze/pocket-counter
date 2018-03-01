from flask import Flask, redirect, session, url_for
from datetime import timedelta
import sys
import config
import client

app = Flask(__name__)

@app.route("/")
def index():
    redirect_uri = url_for('callback', _external=True)
    code = client.get_request_token(config.oauth_request_url, config.consumer_key, redirect_uri)
    session['code'] = code
    return redirect(
        client.build_auth_url(config.authorize_url, code, redirect_uri)
    )

@app.route("/callback")
def callback():
    code = session['code']
    access_token = client.get_token(config.oauth_authorize_url, config.consumer_key, code)

    pocket_list = client.get_list(config.list_url, access_token, config.consumer_key)
    pocket_count = len(pocket_list)
    label_list  = client.get_labels(pocket_list)

    minutes = 0
    for label in label_list:
        minutes += int(''.join(c for c in label if c.isdigit()))

    html = 'Your pocket size: ' + str(pocket_count) + '<br>'
    html += 'Time needs to consume: ' + str(timedelta(minutes=minutes)) + '<br>'
    html += '<a href="/">count it again</a><br><br>'
    html += 'And your list:<br><pre>' + str(label_list) + '</pre>'
    return html

if __name__ == "__main__":
    app.secret_key = config.session_secret
    app.run(host='0.0.0.0', port=4242, debug=False, threaded=True)
