#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given two excel files passed as arguments to the script (e.g., file1, file2),
# create one csv file that combines the excel files on a certain column (e.g., Name). In the yaml file
# you can specify which column you would like to use to combine (as the anchor). By default the 
# column name in the yaml file is the anchor "Name" (which is the column name in both excel files) but you can change it to whatever you want. 
# Also, the script combines tabs (instructor names/codes in our case) and outputs them as rows in the final csv.
# The script outputs a new csv file with a similar name to the original spreadsheet.

# Usage example:
# python process_metadata_ciabatta.py --file1=test_files/consented_students.xlsx --file2=test_files/registrar_file.xlsx --yaml_file=test_files/metadata.yaml 


import argparse
import codecs
import os
import pandas
import re
import sys
import yaml

# define the way we retrieve arguments sent to the script
parser = argparse.ArgumentParser(description='Merge Metadata')
parser.add_argument('--file1', action="store", dest='file1', default='')
parser.add_argument('--file2', action="store", dest='file2', default='')
parser.add_argument('--yaml_file', action="store", dest='yaml_file', default='')
args = parser.parse_args()

# function that flattens the tabs from the excel file
def flatten_tabs(file, new_name):
    tabs = file.sheet_names

    flatten_file = pandas.DataFrame()
    for t in tabs:
        print("Getting data from " + t + " tab")
        this_tab_data = pandas.read_excel(file, t)
        this_tab_data[new_name] = t
        flatten_file = pandas.concat([flatten_file, this_tab_data])

    return(flatten_file)

# open and read the files passed as arguments only if they have .xls or .csv extensions
if args.file1 and args.file2 and args.yaml_file:
    if '.xls' in args.file1:
        file1 = pandas.ExcelFile(args.file1)
    elif '.csv' in args.file1:
        file1_data = pandas.read_csv(args.file1, index=False)

    if '.xls' in args.file2:
        file2 = pandas.ExcelFile(args.file2)
    elif '.csv' in args.file2:
        file2_data = pandas.read_csv(args.file2, index=False)

    # open and read yaml file
    yaml_file = open(args.yaml_file, "r")
    yaml_contents = yaml.load(yaml_file, Loader = yaml.FullLoader)

    # check if file 1 needs to be flatten
    new_column_name = yaml_contents["file_1"]["tab"]
    if new_column_name:
        file1_data = flatten_tabs(file1, new_column_name)
    else:
        file1_data = pandas.read_excel(file1)

    # check if file 2 needs to be flattened
    new_column_name = yaml_contents["file_2"]["tab"]
    if new_column_name:
        file2_data = flatten_tabs(file2, new_column_name)
    else:
        file2_data = pandas.read_excel(file2)
        
    # combine the file on the column "Name"
    combined_file = file1_data.join(file2_data.set_index('Name'), on='Name',
    lsuffix='_file1', rsuffix='_file2')

    combined_file.to_csv("metadata.csv", index=False)

else:
    print('You need to supply a file1, file2, and a yaml file')
