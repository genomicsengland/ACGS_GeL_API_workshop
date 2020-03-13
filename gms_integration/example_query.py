import requests
import time
from CIPAPI_Token import Token

client_id = ""
client_secret = ""

# Urls for beta testing:
auth_url = 'https://login.microsoftonline.com/afee026d-8f37-400e-8869-72d9124873e4/oauth2/token'
cipapi_base_url = 'https://cipapi-gms-beta.genomicsengland.nhs.uk/api/2/'

# Urls for production:
# auth_url = 'https://login.microsoftonline.com/0a99a061-37d0-475e-aa91-f497b83269b2/oauth2/token'
# cipapi_base_url = 'https://cipapi.genomicsengland.nhs.uk/api/2/'


# Generate a token
t = Token(client_id, client_secret, auth_url)

# Get interpretation request list using the token
int_request_list = requests.get(
    cipapi_base_url + 'interpretation-request',
    headers={"Authorization": "JWT " + t.token()}
).json()

print(len(int_request_list['results']))

example_date = "08-02-20"
# example_date = "13-03-20"
date_last_queried_cip_api = time.strptime(example_date, "%d-%m-%y")

# print(date_last_queried_cip_api)
# Loop through interpretation request list pulling interpretation request for each case using the same token
# Token expiry time will be checked with each call, and refreshed automatically if needed
ir_jsons = []
for case in int_request_list['results']:
    url = cipapi_base_url + 'interpretation-request/{case_id}/{case_version}?reports_v6=True'.format(
                case_id=case['interpretation_request_id'].split('-')[0],
                case_version=case['interpretation_request_id'].split('-')[1])
    print(url)

    ir = requests.get(url, headers={"Authorization": "JWT " + t.token()}).json()

    last_modified = time.strptime(ir['last_modified'], "%Y-%m-%dT%H:%M:%S.%fZ")

    if last_modified > date_last_queried_cip_api:
        print(ir['interpretation_request_id'], 'added to list of new cases')
        ir_jsons.append(ir)
    else:
        print(ir['interpretation_request_id'], 'not changed since last updated on {date}'.format(date=example_date))

print(len(ir_jsons))
