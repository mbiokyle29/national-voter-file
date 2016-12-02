# file national-voter-file/src/main/python/NewYorkPrepare.py
"""
New York Prepare.py

This script pre-processes the New York voter file to use usaddress module
to break the address string into standard parts
Also uses the residential address if no mailing address is provided

Outputs lines that fail the address parser to an error log file
"""
import argparse
import collections
import csv
import logging, logging.config
import os
import re
import sys
import usaddress
from datetime import datetime

import PrepareUtils
from settings import LOG_SETTINGS, NY_INPUT_FIELD_NAMES

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger(__name__)

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(description="Process New York State data files")
    parser.add_argument("input_file", help="Input data file")
    parser.add_argument("--output-file", help="Name/Path for output file")
    parser.add_argument("--err-file", help="Name/Path for error file")
    args = parser.parse_args()

    inputFile = os.path.abspath(args.input_file)

    outputFile = args.output_file if args.output_file is not None else "{}._OUT.tsv".format(os.path.splitext(inputFile)[0])
    errorFileName = args.err_file if args.err_file is not None else "{}._ERR.tsv".format(os.path.splitext(inputFile)[0])

    logger.info("Reading from input file {} to output file {}".format(inputFile, outputFile))

    with open(inputFile, encoding='latin-1') as csvfile, open(outputFile, 'w') as outfile, open(errorFileName, 'w') as errorFile:

        reader = csv.DictReader(csvfile, dialect='excel', fieldnames=NY_INPUT_FIELD_NAMES)
        writer = csv.DictWriter(outfile, fieldnames=PrepareUtils.constructOutputFieldNames())
        writer.writeheader()

        # Create a file for writing addresses that don't parse
        errnames = list(PrepareUtils.constructOutputFieldNames())
        errnames.extend(['PARSED_STRING', 'ORIGINAL_TEXT'])
        errWriter = csv.DictWriter(errorFile, fieldnames=errnames)
        errWriter.writeheader()

        for row in reader:

            # Skip blank lines
            if row['MAILADD4'] is None:
                logger.error("Bad row detected!")
                for key in row:
                    logger.error("{}: {}".format(key, row[key] if row[key] is not None else 'NONE'))
                sys.exit()

            outrow = constructVoterRegOutrow(row)

            try:
                addr = constructResidenceAddress(row)
                tagged_address, address_type = usaddress.tag(addr)
                PrepareUtils.appendParsedFields(outrow, tagged_address)

                appendMailingAddress(outrow, row)
                appendJurisdiction(outrow, row)

                writer.writerow(outrow)

            # Gets thrown when the US Address parser gets hopelesly confused. Write this out to the errorFile
            # for manual training later
            except usaddress.RepeatedLabelError as e :
                logger.warn("RepeatedLabelError caught: {} {}".format(e.parsed_string, e.original_string))
                outrow.update({'PARSED_STRING':e.parsed_string,
                               'ORIGINAL_TEXT':e.original_string})

                errWriter.writerow(outrow)


def prepareDate(nyDate):
    return datetime.strptime(nyDate, "%Y%m%d").strftime("%Y-%m-%d")


def appendMailingAddress(outrow, row):
    try:
        tagged_address, address_type = usaddress.tag(' '.join([row['MAILADD1'],
                                                               row['MAILADD2'],
                                                               row['MAILADD3'],
                                                               row['MAILADD4']]))
    except usaddress.RepeatedLabelError as e :
        logger.warn("Can't parse mailing address. Falling back to residential: {}".format(e.original_string))
        tagged_address = {}

    if(len(tagged_address) > 0):
        PrepareUtils.appendMailingAddressFromTaggedFields(outrow, tagged_address, address_type)

    else:
        outrow.update({'MAIL_ADDRESS_LINE1': PrepareUtils.constructMailAddr1FromOutRow(outrow),
                       'MAIL_ADDRESS_LINE2': PrepareUtils.constructMailAddr2FromOutRow(outrow),
                       'MAIL_CITY': outrow['PLACE_NAME'],
                       'MAIL_STATE': outrow['STATE_NAME'],
                       'MAIL_ZIP_CODE': outrow['ZIP_CODE'],
                       'MAIL_COUNTRY': 'USA'})


def appendJurisdiction(outrow, row):
        outrow.update({
        'COUNTYCODE':row['COUNTYCODE'],
        'CONGRESSIONAL_DIST':row['CD'],
        'UPPER_HOUSE_DIST':row['SD'],
        'LOWER_HOUSE_DIST':row['AD']})


def constructResidenceAddress(row):
    aptField = row['RAPARTMENT'].strip()
    return ' '.join([row['RADDNUMBER'],
                     row['RHALFCODE'],
                     row['RPREDIRECTION'],
                     row['RSTREETNAME'],
                     row['RPOSTDIRECTION'],
                     'Apt ' + row['RAPARTMENT'] if aptField and aptField != 'APT' else ''])


def constructVoterRegOutrow(row):
    return {'STATE_VOTER_REF': row['SBOEID'],
            'COUNTY_VOTER_REF': row['COUNTYVRNUMBER'],
            'FIRST_NAME': row['FIRSTNAME'],
            'MIDDLE_NAME': row['MIDDLENAME'],
            'LAST_NAME': row['LASTNAME'],
            'NAME_SUFFIX': row['NAMESUFFIX'],
            'BIRTHDATE': prepareDate(row['DOB']),
            'GENDER':  row['GENDER'],
            'REGISTRATION_DATE': prepareDate(row['REGDATE']),
            'REGISTRATION_STATUS': row['STATUS'].strip(),
            'PARTY': (row['ENROLLMENT'] if row['ENROLLMENT'] != 'OTH' else row['OTHERPARTY']),
            'PLACE_NAME': row['RCITY'].upper(),
            'STATE_NAME': 'NY',
            'ZIP_CODE': row['RZIP5']}


if __name__ == "__main__":
    main()
