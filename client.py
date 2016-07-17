import urllib
import urllib2
import urlparse

def get_request_token(code_url, consumer_key, redirect_uri):

	post_params = {
		'consumer_key': consumer_key,
		'redirect_uri': redirect_uri
	}

	request = urllib2.Request(code_url, urllib.urlencode(post_params))
	response = urllib2.urlopen(request)

	raw_response = response.read()
	response_body = dict(urlparse.parse_qsl(raw_response))
	return response_body.get('code')

def build_auth_url(auth_url, code, redirect_uri):
	return auth_url + '?' + urllib.urlencode({'request_token': code, 'redirect_uri': redirect_uri})
#	return auth_url + '?request_token=' + code + '&redirect_uri=' + redirect_uri