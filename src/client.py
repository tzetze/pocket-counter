import urllib
import urllib2
import urlparse
import json

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
    auth_params = {
        'request_token': code,
        'redirect_uri': redirect_uri
    }
    return auth_url + '?' + urllib.urlencode(auth_params)

def get_token(auth_url, consumer_key, code):
    post_params = {
        'consumer_key': consumer_key,
        'code': code
    }

    request = urllib2.Request(auth_url, urllib.urlencode(post_params))
    response = urllib2.urlopen(request)

    raw_response = response.read()
    response_body = dict(urlparse.parse_qsl(raw_response))
    return response_body.get('access_token')

def get_labels(pocket_list):
    taglist = []
    for entry in pocket_list.itervalues():
        print str(entry) + "\n\n"
        if 'tags' in entry:
            for label in entry['tags']:
                if ' minutes' in label:
                    taglist.append(label)
    return taglist

def get_list(list_url, access_token, consumer_key):
    list_params = {
        'access_token': access_token,
        'consumer_key': consumer_key,
        'count': 10000,
        'detailType': 'complete'
    }
    request = urllib2.Request(list_url, urllib.urlencode(list_params))
    response = urllib2.urlopen(request)

    raw_response = response.read()
    response_data = json.loads(raw_response)
    return response_data.get('list')
