"""
This is some examples prepared for a CIP-API Surgery Call on 11/09/2020

It is a guide only, not tested and should not be used "as is" without further review

"""
import os
import requests


host_gms = f"https://cipapi-gms-beta.genomicsengland.nhs.uk" # update this for prod

tenant_id = "update this" # see here: https://ip-cipapi-help.genomicsengland.co.uk/3.15/environments/

# environment variables set with client ID and secret, these will have been shared by GeL Service Desk
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_client_creds_ad_token(tenant_id, client_id, client_secret):

    """

    NOTE!! this is a simple method that should not be used in production

    """

    url = "https://login.microsoftonline.com/{tenant_id}/oauth2/token".format(tenant_id=tenant_id)

    payload = "grant_type=client_credentials"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    response = requests.request("POST", url, data=payload, headers=headers, auth=(client_id, client_secret)).json()

    return response


def list_cases(token):

    """

    Return a list of cases from the CIP-API with some different params

    interpreter_organisation_national_grouping_id will always be the GLH

    """

    # some different examples made to the list end point
    url = '{host}/api/2/interpretation-request'.format(host=host_gms)
    # url = '{host}/api/2/interpretation-request?extra-params=show_referral'.format(host=host_gms)
    # url = '{host}/api/2/interpretation-request?extra-params=show_referral&primary_glh_cases=True'.format(host=host_gms)
    # url = '{host}/api/2/interpretation-request?extra-params=show_referral&category=gms&interpreter_organisation_national_grouping_id=69A70'.format(host=host_gms)

    auth_header = {'Authorization': 'JWT {}'.format(token)}
    case_list = requests.get(url, headers=auth_header).json()
    return case_list


def get_unique_interpreter_ids(case_list):

    """ for a list of cases returned from the CIP-API get return a unique list of GLHs IDs aka
    interpreter_organisation_national_grouping_id"""

    id_list = []

    referrals = [x['referral'] for x in case_list['results']]

    referral_tests = [x['referral_test'] for x in referrals]

    for referral_test in referral_tests:
        for test in referral_test:
            id_list.append(test['interpreter_organisation_national_grouping_id'])

    return set(id_list)


def get_pid(referral_data):

    """ Example getting PID using the same token used to query AD

    NOTE! to get PID the referral information must exist in the BETA(UAT) instance of TOMS

    """

    referral_uid = referral_data['referral_uid']

    url = "https://api.beta.genomics.nhs.uk/reidentification/referral-pid/{referral_uid}".format(referral_uid=referral_uid)

    auth_header = {'Authorization': 'Bearer {}'.format(jwt_token)}

    pid = requests.get(url, headers=auth_header).json()

    return pid


if __name__ == "__main__":

    d = get_client_creds_ad_token(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
    jwt_token = d['access_token']

    case_list = list_cases(jwt_token)

    print(get_unique_interpreter_ids(case_list))

    referral_data = case_list['results'][0]['referral']

    print(get_pid(referral_data))