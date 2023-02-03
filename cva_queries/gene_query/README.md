# CVA Gene Query

The following script queries Genomics England Clinical Variant Ark [CVA](https://ip-cva-help.genomicsengland.co.uk/) for
a specified gene symbol and checks if that gene contains any tier 1 or tier 2 variants.

## Pre-requisites 

Tested using Python 3.8 (Note! Python 3.10 does not work)

`pip install clinical-variant-ark`

You will need to be on the HSCN network and have a CVA username and password

## Running the script

`python cva_gene_query.py -g ENSG00000142168 -u gene.helix@nhs.net -o ~/Desktop -p`

Where:

- “-g ENSG00000142168” is the ensembl gene for SOD1 (or your gene of interest)
- “-u “ is your cva username
- “-o” is the location of where you want to output file to save
- “-p” is prompt for your CVA password

The output file will contain a list of cases that contain a tier 1 or tier 2 variant in the gene specified.

NOTE! The output contains the cva_status which is NOT specific to the variants in the gene specified

If your gene contains lots of cases / variants the script my timeout, this is a known issue with the clinical variant
ark python package that needs fixing!