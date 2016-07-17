from flask import Flask, redirect
import sys
import config
import client

app = Flask(__name__)


@app.route("/")
def index():
	code = client.get_request_token(config.code_url, config.consumer_key, config.redirect_uri)
	return redirect(
		client.build_auth_url(config.auth_url, code, config.redirect_uri)
	)

@app.route("/callback")
def callback():
	return 'returned!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4242, debug=False)
