#!/usr/bin/env python
#**************************************************************************************
#**************************************************************************************
#  schizconnect_dd_to_json.py
#  License: GPL
#**************************************************************************************
#**************************************************************************************
# Date: 10-15-19                 Coded by: David Keator (dbkeator@gmail.com)
# Filename: schizconnect_dd_to_json.py
#
# Program description:  This program will load in schizconnect XLSX data dictionary
# files and convert them to a JSON representation for use in PyNIDM tools csv2nidm and
# bidsmri2nidm
#
#**************************************************************************************
# Development environment: Python - PyCharm IDE
#
#**************************************************************************************
# System requirements:  Python 3.X
# Libraries:
#**************************************************************************************
# Start date: 10-15-19
# Update history:
# DATE            MODIFICATION				Who
#
#
#**************************************************************************************
# Programmer comments:
#
#
#**************************************************************************************
#**************************************************************************************


import os,sys
from argparse import ArgumentParser
from os.path import  dirname, join, splitext
import pandas as pd
import json
import uuid
import pyld



def main(argv):
    parser = ArgumentParser(description='This program will load in schizconnect XLSX data dictionary \
    files and convert them to a JSON representation for use in PyNIDM tools csv2nidm and \
    bidsmri2nidm.  See "examples" directory for example XLSX files and format supported')

    parser.add_argument('-xls', dest='xls_file', required=True, help="XLS/XLSX Excel file to convert")
    parser.add_argument('-o', dest='out_dir', required=True, help='''Output directory where each Instrument will
                                                                  be stored as a different JSON file''')

    args = parser.parse_args()

    # open XLS file
    xlsdf = pd.read_excel(args.xls_file,header=0)

    # XLS file has columns "Instrument", "Question Label", Question Description, Question ID, Response Label,
    # Response Value, Response Description

    # jsondf = xlsdf.to_json(orient='records')
    # with open(join(args.out_dir, 'test.json'), 'w') as outfile:
    #    json.dump(jsondf, outfile)

    json_dict = {}

    context = {}
    context['@version'] = 1.1
    context.update({
        "niiri": {"@type": "@id","@id":"http://iri.nidash.org/"},
    })

    for index,row in xlsdf.iterrows():

        # check if instrument name is null, if so we're still collecting questions of instrument
        if not pd.isnull(row['Instrument']):
            current_assessment = str(row['Instrument'])
            # create dictionary entry for assessment
            json_dict[current_assessment] = {}
            # create place holder for isAbout
            # json_dict[row['Instrument']]['isAbout'] = ''
            json_dict[current_assessment]['dct:identifier'] = "http://iri.nidash.org/" + str(uuid.uuid1())
            json_dict[current_assessment]['rdfs:label'] = str(row['Instrument'])
            json_dict[current_assessment]['Questions'] = {}

            # first question of each assessment is on the same row as assessment name
            if not pd.isnull(row['Question ID']):
                current_question_id = str(row['Question ID'])
                json_dict[current_assessment]['Questions'][current_question_id] = {}
                json_dict[current_assessment]['Questions'][current_question_id]['skos:preflabel'] = current_question_id
                if not pd.isnull(row['Question Label']):
                    json_dict[row['Instrument']]['Questions'][current_question_id]['skos:definition'] = str(row['Question Label'])


                if not pd.isnull(row['Response Label']):
                    json_dict[current_assessment]['Questions'][current_question_id]['categories'] = {}
                    json_dict[current_assessment]['Questions'][current_question_id]['categories'][str(row['Response Value'])] = str(row['Response Label'])
                if not pd.isnull(row['Question Description']):
                    json_dict[current_assessment]['Questions'][current_question_id]['rdf:description'] = str(row['Question Description'])


        else:
            # this is a row without an instrument name in the 1st column then it's within the "current_assessment"
            if pd.isnull(row['Question Label']) and pd.isnull(row['Question ID']):
                # same question label and ID so this must be simply storing responses
                json_dict[current_assessment]['Questions'][current_question_id]['categories'][str(row['Response Value'])] = str(row['Response Label'])
            elif not pd.isnull(row['Question Label']):
                # then this is a new question so set up the structure and continue
                if not pd.isnull(row['Question ID']):
                    current_question_id = str(row['Question ID'])
                    json_dict[current_assessment]['Questions'][current_question_id] = {}
                    json_dict[current_assessment]['Questions'][current_question_id]['skos:preflabel'] = current_question_id
                    if not pd.isnull(row['Question Label']):
                        json_dict[current_assessment]['Questions'][current_question_id]['skos:definition'] = str(row['Question Label'])

                    if not pd.isnull(row['Response Label']):
                        json_dict[current_assessment]['Questions'][current_question_id]['skos:definition'] = str(row['Question Label'])
                    if not pd.isnull(row['Question Description']):
                        json_dict[current_assessment]['Questions'][current_question_id]['rdf:description'] = str(row['Question Description'])


                    if not pd.isnull(row['Response Label']):
                        json_dict[current_assessment]['Questions'][current_question_id]['categories'] = {}
                        json_dict[current_assessment]['Questions'][current_question_id]['categories'][str(row['Response Value'])] = str(row['Response Label'])


    with open(join(args.out_dir, 'test.json'), 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)
    compacted = pyld.jsonld.compact(json_dict,context)
    print(compacted)
    with open(join(args.out_dir, 'test.jsonld'), 'w') as outfile:
        json.dump(compacted,outfile, indent=4)


if __name__ == "__main__":
   main(sys.argv[1:])
