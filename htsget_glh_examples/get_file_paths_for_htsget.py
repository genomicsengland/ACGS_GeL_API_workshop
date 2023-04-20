import os
import requests

STUDY_ID_LOOKUP_DICT = {"RD38GMS": 1053593329}  # this is environment specific

def get_client_creds_ad_token(tenant_id, client_id, client_secret):

    """
    NOTE!! this is a simple method that should not be used in production
    """

    url = "https://login.microsoftonline.com/{tenant_id}/oauth2/token".format(
        tenant_id=tenant_id
    )

    payload = "grant_type=client_credentials"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, auth=(client_id, client_secret)
    ).json()

    return response


def get_url_json_response(url):
    response = requests.get(url=url, headers={"Authorization": 'JWT "TOKEN"'})

    if response.status_code != 200:
        raise ValueError(
            "Received status: {status} for url: {url} with response: {response}".format(
                status=response.status_code, url=url, response=response.content
            )
        )
    return response.json()


def get_htsget_urls(path_prefix, htsget_server, payload, type, chrom, start, end):
    """
    path_prefix: file paths in the CIP-API payload have a prefix that needs removing to work with HTSget
    htsget_server: the instance of HTSget
    payload: json payload from the CIP-API
    type: either "reads" or "variants" for bams(crams) and vcfs respectively
    chrom: chromosome in format 22 rather than chr22, of the region want to query
    start: start position of region want to query
    end: end position of region want to query


    """

    location = f"?referenceName={chrom}&start={str(start)}&end={str(end)}"

    study_id = STUDY_ID_LOOKUP_DICT[payload["internalStudyId"]]

    htsget_url = f"{htsget_server}/{type}/bypath/{study_id}/"

    htsget_file_path_dict = {}

    type_dict = {"reads": "bams", "variants": "vcfs"}

    htsget_file_path_dict[type_dict[type]] = [
        os.path.join(
            htsget_url,
            os.path.relpath(x["uriFile"], path_prefix).replace("/", ":") + location,
        )
        for x in payload[type_dict[type]]
    ]

    return htsget_file_path_dict


if __name__ == "__main__":

    # path_prefix = '/genomes/bertha-prod' # you will need to alter this based on what the prefix is in the payload file paths, generally in prod it will be this '/genomes/bertha-prod'
    path_prefix = "/genomes/bertha-test"

    htsget_server = "https://htsget-gms-beta.genomicsengland.nhs.uk"  # this is the uat instance of HTSget
    # htsget_server = 'https://htsget.genomicsengland.nhs.uk'

    # for examples of how to obtain payloads from CIP-API see: https://github.com/genomicsengland/ACGS_GeL_API_workshop/blob/master/CIP_API_examples.ipynb
    # for full docs see: https://ip-cipapi-help.genomicsengland.co.uk/
    ir_id = "1234"
    ir_version = "1"
    chrom = "22"
    start = 23180509
    end = 23280509
    CIP_API_SERVER_URL = "https://cip-host-name/api/{endpoint}"
    ir_case_url = CIP_API_SERVER_URL.format(
        endpoint="interpretation-request/{ir_id}/{ir_version}/"
    )
    ir_case_url = ir_case_url.format(ir_id=ir_id, ir_version=ir_version)
    payload = get_url_json_response(url=ir_case_url)

    for type in ["reads", "variants"]:
        htsget_urls = get_htsget_urls(
            path_prefix=path_prefix,
            htsget_server=htsget_server,
            type=type,
            payload=payload["interpretation_request_data"]["json_request"],
            chrom=chrom,
            start=start,
            end=end,
        )
        print(htsget_urls)
