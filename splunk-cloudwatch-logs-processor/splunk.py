#!  /usr/bin/env python3

import base64
import boto3
import gzip
import json
import os
import requests
import sys
import urllib3

#   Disable warnings about SSL certificates.
urllib3.disable_warnings()

# Read SSM prefix and Splunk cache TTL from environment.
SSM_PREFIX       = os.environ.get('SSM_PREFIX', '/cloudwatch_to_splunk')
SPLUNK_CACHE_TTL = os.environ.get('SPLUNK_CACHE_TTL', 6 * 1000)

client = boto3.client('ssm')

#   FIXME: Should event data be read in text mode or binary mode?

#####

def get_splunk_logger(parsed, context):
    log_group = parsed["logGroup"]

    # FIXME: hack:
    log_group = '/service/authman'

    print('{:<12} = {}'.format('log_group', log_group))

    ssm_path = SSM_PREFIX + log_group

    print('{:<12} = {}'.format('ssm_path', ssm_path))

    names = \
        [
        '/'.join((ssm_path, 'hec_endpoint')),
        '/'.join((ssm_path, 'hec_token')),
        '/'.join((ssm_path, 'sourcetype'))
        ]

    #   FIXME: check for failure.
    response = client.get_parameters(Names=names, WithDecryption=True)
    response_dict = ssm_response_to_dict(ssm_path, response)

    for name, value in sorted(response_dict.items()):
        print(f'{name:<12} = {value}')
    return

#####

def handler(event, context):
    print('Received event:', json.dumps(event, indent=2))
    print('Received context:', json.dumps(context, indent=2))

    # Decode base64-encoded CloudWatch log data.
    payload = base64.b64decode(event['awslogs']['data'])

    # Decompress gzipped payload and parse resulting JSON.
    result = gzip.decompress(payload)
    parsed = json.loads(result)
    print('Decoded payload:', json.dumps(parsed, indent=2))

    get_splunk_logger(parsed, context)
    return

#####

def ssm_response_to_dict(ssm_path, response):
    ssm_dict = dict()

    for parm in response['Parameters']:
        name, value = parm.get('Name'), parm.get('Value')

        # FIXME: replace with better exception
        if name.index(ssm_path) != 0:
            raise Exception('BAD VALUE')

        name = name[1 + len(ssm_path):]
        ssm_dict.update({ name : value })
        
    return ssm_dict

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
