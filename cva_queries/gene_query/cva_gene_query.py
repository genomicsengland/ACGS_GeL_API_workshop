import requests
import os
from pyark.cva_client import CvaClient
from datetime import datetime
import csv
import argparse
import getpass

"""

Script that queries CVA for a gene symbol and checks if that gene contains any tier1 or tier2 variants

"""


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

    if len(case_variants["response"]) == 1:
        return True
    else:
        print("error, more / less variants returned than expected!!")
        return False


def parse_case_variants(case_id, case_variants, gene_symbol):
    """

    :param case_id:
    :param case_variants:
    :param gene_symbol:
    :return:
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


def get_case_variants(case_list):
    output = []
    total_cases = len(case_list)
    counter = 0
    print(total_cases, 'cases found in CVA')
    for case in case_list:
        counter += 1
        case_id = "-".join([str(case["identifier"]), str(case["version"])])
        print(f'Checking case {str(counter)} ({case_id}) for tier 1 and tier 2 variants...')
        # get all the variants in a specific case
        new_url = f"{HOST}cva/api/0/cases/{str(case['identifier'])}/{str(case['version'])}/variants"
        x = requests.get(url=new_url, headers={"Authorization": cva._token}).json()
        case_gene_variants = parse_case_variants(
            case_id=case_id, case_variants=x, gene_symbol=gene_symbol
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

    with open(output_file_name, "w") as f_handle:
        line_writer = csv.writer(f_handle, delimiter=",")
        header = [
            "#group_id",
            "category",
            "cva_status",
            "variant",
            "highest_tier",
            "#case_link",
        ]
        line_writer.writerow(header)
        for case in case_variant_list:
            line_writer.writerow(case)

    return output_file_name


if __name__ == "__main__":

    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    HOST = "https://cva.genomicsengland.nhs.uk/"
    args = parse_arguments()

    gene_symbol = args.gene
    # password = ""

    if args.password:
        password = getpass.getpass()

    cva = CvaClient(url_base=HOST, user=args.username, password=password)

    cases_client = cva.cases()
    # get a list of cases that have a variant in specified gene symbol
    case_list = list(cases_client.get_cases(genes=[gene_symbol]))
    case_variants = get_case_variants(case_list=case_list)
    f_name = f"cva_{gene_symbol}_{date}.csv"
    output_file_name = os.path.expanduser(os.path.join(args.output_dir, f_name))
    output = write_output_file(
        case_variant_list=case_variants, output_file_name=output_file_name
    )
    print(output)
