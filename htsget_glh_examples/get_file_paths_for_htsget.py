"""
Example script to make a request to the CIP-API for an interpretation request

Get the Interpretation Request Data and the paths to the BAM and VCF files

Reformat the file paths so that they are HTSget compatible

Construct the HTSget URLs

Which can then be used in IGV

"""
import os
import requests


def get_client_creds_ad_token(tenant_id, client_id, client_secret):
    """
    NOTE!! this is a simple method that should not be used in production

    Args:
        client_secret:
        client_id:
        tenant_id (object):
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

    return response["access_token"]


def get_interpretation_request_data(host, token, case_id, case_version):
    """Basic function to get an interpretation request payload for a specific case
    The payload contains the BAM and VCF paths that are needed for HTSget
    """

    url = f"{host}/api/2/interpretation-request/{case_id}/{case_version}"

    auth_header = {"Authorization": "JWT " + token}

    interpretation_request = requests.get(url, headers=auth_header).json()

    return interpretation_request["interpretation_request_data"]["json_request"]


def remove_unwanted_mount_from_file_path(file_path_with_mount, path_prefix):
    removed_mount = os.path.relpath(file_path_with_mount, path_prefix)
    return removed_mount


def replace_slash_with_colon_in_file_path(slash_file_path):
    colon_file_path = slash_file_path.replace("/", ":")
    return colon_file_path


def create_htsget_url_with_reads_or_variants(host, type):
    htsget_url = f"{host}/{type}/bypath/"

    return htsget_url


def get_opencga_study_id_from_cipapi_payload(payload, study_id_lookup):
    study_id = study_id_lookup[payload["internalStudyId"]]

    return str(study_id)


def get_htsget_url(htsget_base_url, opencga_study_id, file_path_for_htsget):
    return os.path.join(htsget_base_url, opencga_study_id, file_path_for_htsget)


def get_htsget_type(file_type):
    if file_type == "bams":
        return "reads"
    elif file_type == "vcfs":
        return "variants"


def get_cram_htsget_links_for_payload(
    payload, path_prefix, htsget_server, study_id_lookup
):
    htsget_links = []
    for file_type in ["bams", "vcfs"]:
        htsget_type = get_htsget_type(file_type=file_type)

        for file_object in payload[file_type]:
            mount_removed_file_path = remove_unwanted_mount_from_file_path(
                file_path_with_mount=file_object["uriFile"], path_prefix=path_prefix
            )
            file_path_for_htsget = replace_slash_with_colon_in_file_path(
                mount_removed_file_path
            )
            htsget_base_url = create_htsget_url_with_reads_or_variants(
                host=htsget_server, type=htsget_type
            )

            opencga_study_id = get_opencga_study_id_from_cipapi_payload(
                payload=payload, study_id_lookup=study_id_lookup
            )

            htsget_link = get_htsget_url(
                htsget_base_url=htsget_base_url,
                opencga_study_id=opencga_study_id,
                file_path_for_htsget=file_path_for_htsget,
            )
            htsget_links.append(htsget_link)

    return htsget_links


def create_location_string(chrom, start, end):
    return f"?referenceName={chrom}&start={str(start)}&end={str(end)}"


if __name__ == "__main__":
    TYPE_DICT = {"reads": "bams", "variants": "vcfs"}

    STUDY_ID_LOOKUP_DICT = {
        "RD38GMS": 1053593329
    }  # this is for UAT and is environment specific

    tenant_id = ""
    client_id = ""
    client_secret = ""

    token = get_client_creds_ad_token(
        tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
    )

    host = "https://cipapi-gms-beta.genomicsengland.nhs.uk"
    htsget_server = "https://htsget-gms-beta.genomicsengland.nhs.uk"

    # for examples of how to obtain payloads from CIP-API see: https://github.com/genomicsengland/ACGS_GeL_API_workshop/blob/master/CIP_API_examples.ipynb
    # for full docs see: https://ip-cipapi-help.genomicsengland.co.uk/
    ir_id = "3588"
    ir_version = "1"

    interpretation_request_data = get_interpretation_request_data(
        host=host, token=token, case_id=ir_id, case_version=ir_version
    )

    path_prefix = "/genomes/bertha-test"

    htsget_urls = get_cram_htsget_links_for_payload(
        payload=interpretation_request_data,
        path_prefix=path_prefix,
        htsget_server=htsget_server,
        study_id_lookup=STUDY_ID_LOOKUP_DICT,
    )

    # these can be plugged into the "url" field of the igv_snippet.html

    for htsget_url in htsget_urls:
        print(htsget_url)
