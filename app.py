from flask import Flask, redirect, session, url_for
import sys
import config
import client

app = Flask(__name__)

@app.route("/")
def index():
    redirect_uri = url_for('callback')
    code = client.get_request_token(config.oauth_request_url, config.consumer_key, redirect_uri)
    session['code'] = code
    return redirect(
        client.build_auth_url(config.authorize_url, code, redirect_uri)
    )

@app.route("/callback")
def callback():
    code = session['code']
    access_token = client.get_token(config.oauth_authorize_url, config.consumer_key, code)
    pocket_count = client.get_count(config.list_url, access_token, config.consumer_key)
    return 'Your pocket size: ' + str(pocket_count) + ' <a href="/">again</a>'

if __name__ == "__main__":
    app.secret_key = config.session_secret
    app.run(host='0.0.0.0', port=4242, debug=False, threaded=True)
