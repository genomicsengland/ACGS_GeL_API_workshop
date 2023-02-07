import requests
import os
from pyark.cva_client import CvaClient
from datetime import datetime
import csv
import argparse
import getpass
import logging

"""

Script queries CVA for an Ensembl gene ID and checks if the gene contains any tier1 or tier2 variants.

Produces a .csv output list the cases that have Tier 1 or Tier 2 variants in that gene

Tested on SOD1: ENSG00000142168

python cva_gene_query.py -g ENSG00000142168 -u email@nhs.net -o ~/Desktop -p

"""

HOST = "https://cva.genomicsengland.nhs.uk/"


def parse_arguments():
    parser = argparse.ArgumentParser(
        "Look up CVA variants in a gene (Ensembl ENSG ID) specified and report back any tier 1 or tier 2 variants"
    )
    parser.add_argument(
        "-g",
        "--gene",
        required=True,
        help="ENSG gene symbol e.g. ENSG00000142168 for SOD1",
    )
    parser.add_argument(
        "-u",
        "--username",
        required=True,
        help="CVA Username e.g. email address",
    )
    parser.add_argument(
        "-p",
        "--password",
        action="store_true",
        dest="password",
        help="hidden password prompt",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        required=True,
        help="File directory where output file will be written",
    )
    return parser.parse_args()


def check_response(case_variants):
    """Helper function that checks the response from CVA is looking OK."""

    if "response" in case_variants.keys() and len(case_variants["response"]) == 1:
        return True
    else:
        print("Error, no API response OR more / less variants returned than expected!!")
        return False


def parse_case_variants(case_id, case_variants, gene_symbol):
    """Filters CVA API response to only variants in a specific gene that are tier 1 or tier 2.

    case_id format = 123-1
    case_variants = response from f"{HOST}cva/api/0/cases/{str(case['identifier'])}/{str(case['version'])}/variants"
    gene_symbol = Ensembl ID
    """
    # create CVA url for the case
    cva_case_url = f"{HOST}case/{case_id}"
    gene_variants = []
    if check_response(case_variants):
        for var in case_variants["response"][0]["result"]:
            for gene in var["reportEventGenes"]:
                if gene["ensemblId"] == gene_symbol:
                    for interp in var["interpretations"]:
                        if interp["author"] == "genomics_england_tiering" and interp[
                            "highestTier"
                        ] in ["TIER1", "TIER2"]:
                            variants = [
                                var["grch38DisplayCoordinate"],
                                interp["highestTier"],
                                cva_case_url,
                            ]
                            gene_variants.extend(variants)
    return gene_variants


def get_case_variants(cva_client, gene_symbol):

    """Get all the cases that have variants in the gene symbol specified then checks if variants are tier 1 or tier 2

    Uses the "parse_case_variants()" function to check the tier 1 and tier 2 variants in a case

    :param cva_client: authenicated instance of CvaClient()
    :param gene_symbol: ENSG gene ID
    :return:
    """
    output = []

    cases_client = cva_client.cases()
    # get a list of cases that have a variant in specified gene symbol
    case_list = list(cases_client.get_cases(genes=[gene_symbol]))

    total_cases = len(case_list)
    counter = 0
    print(total_cases, "cases found in CVA")
    logging.info(total_cases, "cases found in CVA")
    for case in case_list:
        counter += 1
        case_id = "-".join([str(case["identifier"]), str(case["version"])])
        print(
            f"Checking case {str(counter)} ({case_id}) for tier 1 and tier 2 variants..."
        )
        logging.info(
            f"Checking case {str(counter)} ({case_id}) for tier 1 and tier 2 variants..."
        )
        # get all the variants in a specific case
        cva_case_variants_url = f"{HOST}cva/api/0/cases/{str(case['identifier'])}/{str(case['version'])}/variants"
        cva_case_variant_data = requests.get(
            url=cva_case_variants_url, headers={"Authorization": cva_client._token}
        ).json()
        case_gene_variants = parse_case_variants(
            case_id=case_id, case_variants=cva_case_variant_data, gene_symbol=gene_symbol
        )
        if len(case_gene_variants) != 0:
            row = [
                case["groupId"],
                case["category"],
                case["summaryStatus"],
            ] + case_gene_variants
            output.append(row)
    return output


def write_output_file(case_variant_list, output_file_name):

    """From the cases identified write a comma sep file that includes link to case in CVA

    NOTE the cva case status is the overall case status and not always relevant to the gene / variant identified

    :param case_variant_list:
    :param output_file_name:
    :return:
    """

    with open(output_file_name, "w") as f_handle:
        line_writer = csv.writer(f_handle, delimiter=",")
        header = [
            "#group_id",
            "category",
            "cva_status",
            "variant",
            "highest_tier",
            "cva_case_link",
        ]
        line_writer.writerow(header)
        for case in case_variant_list:
            line_writer.writerow(case)

    return output_file_name


def main():
    """

    :return:
    """
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    args = parse_arguments()

    gene_symbol = args.gene

    if args.password:
        password = getpass.getpass()

    cva = CvaClient(url_base=HOST, user=args.username, password=password)
    case_variants = get_case_variants(cva_client=cva, gene_symbol=gene_symbol)
    f_name = f"cva_{gene_symbol}_{date}.csv"
    output_file_name = os.path.expanduser(os.path.join(args.output_dir, f_name))
    output = write_output_file(
        case_variant_list=case_variants, output_file_name=output_file_name
    )
    return output


if __name__ == "__main__":

    main()
