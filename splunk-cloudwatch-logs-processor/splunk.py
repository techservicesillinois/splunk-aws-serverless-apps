#!  /usr/bin/env python3

import json
import requests
import sys
import urllib3

#   Disable warnings about SSL certificates.
urllib3.disable_warnings()

TOKEN   = '8153ebc9ffc57baa8e864e3495fbc20a53604bc52774ab5d3a84599cb47925f6:0c423f54-c572-474f-8789-43e23726aae5'
URL     = 'https://dspbeta04.dsp-hec.api.scp.splunk.com/services/collector'

#####

def handler(event, context):
    pass

#####

def event_to_splunk(url, token, data):
    headers = dict(Authorization='Splunk dsphec:' + token)
    print('headers', headers)
    print('data', data)
    print()

    print('{:<20} = {}'.format('url', url))

    response = requests.post(url, headers=headers, json=data, verify=False)

#   request = response.request
#   print('request.body', request.body)
#   print('{:<20} = {}'.format('request.body', request.body))
#   print('request.headers', request.headers)
#   print('request.method', request.method)
#   print()

#   print('{:<20} = {}'.format('response.content', response.content))
#   print('{:<20} = {}'.format('response.cookies', response.cookies))
#   print('{:<20} = {}'.format('response.headers', response.headers))
#   print('{:<20} = {}'.format('response.json', response.json()))
    print('{:<20} = {}'.format('response.ok', response.ok))
    print('{:<20} = {}'.format('response.reason', response.reason))
    print('{:<20} = {}'.format('response.status_code', response.status_code))
    print('{:<20} = {}'.format('response.text', response.text))
#   print('response.url', response.url)
    return

def main(argv):
    text = \
    '''
    We the People of the United States, in Order to form a more perfect Union,
    establish Justice, insure domestic Tranquility, provide for the common
    defence, promote the general Welfare, and secure the Blessings of
    Liberty to ourselves and our Posterity, do ordain and establish this
    Constitution for the United States of America.
    '''

    text_list = [l.strip() for l in text.splitlines() ]

    payload = dict(sourcetype='test')
    payload.update(event=text_list)
    print('payload', json.dumps(payload))
    print()

    event_to_splunk(URL, TOKEN, payload)
    return 0

#####

if __name__ == '__main__':
    sys.exit(main(sys.argv))
