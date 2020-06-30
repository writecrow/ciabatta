#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


# DESCRIPTION:
# Given a folder with .txt files (inlcuding subfolders),
# the script removes lines before the body of the student texts that have names, initials, emails, etc.
# Disclaimer: this script deletes conseutive capitalized words and might delete assignment titles


# Usage example:
# Run this line below from the terminal on a Mac or command prompt on Windows
# Mac example: python ciabatta_deid.py --directory=../../../spring_2018/files_with_headers/
# PC example: python ciabatta_deid.py --directory=..\..\..\spring_2018\files_with_headers\
# what follows --directory= is the folder with the files on your computer which you need to specify


#import packages
import argparse
import os
import re

# Lists the required arguments (e.g. --directory=) sent to the script
parser = argparse.ArgumentParser(description='De-identify Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action='store', dest='dir', default='')
args = parser.parse_args()

# function to remove any name patterns from a line of text
def clean_names_from_line(original_line):
    # cleans white space and line break in lines before text body
    cleaned_line = re.sub(r'(\r+)?\n', r'', original_line)

    # removes any initials like H. and j.
    cleaned_line = re.sub(r'\s[A-Za-z]\.', r'', cleaned_line)

    # removes titles and other identifiers
    cleaned_line = re.sub(r'name|net\s?id|id|student|professor|prof\.|teacher|instructor|Mr\.|Dr\.|Mr?s\.|[A-Z]\.|\s[A-Za-z]\s', r'', cleaned_line, flags=re.IGNORECASE)

    # removes any remaining punctuation
    cleaned_line = re.sub(r'(,|\.|\:)', r'', cleaned_line)

    # removes name and last name
    cleaned_line = re.sub(r'(([A-Z][a-z]+\s+){1,3})?[A-Za-z]+', r'', cleaned_line)

    # remove numbers
    cleaned_line = re.sub(r'[0-9]+', r'', cleaned_line)

    # remove any extra spaces
    cleaned_line = re.sub(r'\s', r'', cleaned_line)
    cleaned_line = cleaned_line.strip()

    # return the line with name patterns removed
    return(cleaned_line)

# function to remove any email address patterns from a line of text
def clean_email_from_line(original_line):
    cleaned_line = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'', original_line)
    # remove any extra spaces
    cleaned_line = re.sub(r'\s', r'', cleaned_line)
    cleaned_line = cleaned_line.strip()

    # return the line with name patterns removed
    return(cleaned_line)


# creates a function that deidentifies each individual file
def deidentify_file(filename, overwrite=False):
    # only works with .txt files
    found_text_files = False
    if '.txt' in filename:
        found_text_files = True
        # deletes slashes and periods from the filename path ../../../spring_2018/files_with_headers/
        cleaned_filename2 = re.sub(r'\.\.[\\\/]', r'', filename)

        # creates output directory
        output_directory = 'deidentified'

        # creates new files with the same name as original files in the "deidentified" output directory
        output_filename = os.path.join(output_directory, cleaned_filename2)

        # creates directory inside the "deidentified" directory with the same name as original directory
        directory = os.path.dirname(output_filename)

        # if output directory does not exist already, it creates one
        if not os.path.exists(directory):
            os.makedirs(directory)

        # opens and reads in the file
        textfile = open(filename, 'r')
        # opens the output file and writes in it
        output_file = open(output_filename, "w")

        found_text_body=False
        # loops through every line in the file
        for line in textfile:
            # strips spaces at the end of the line
            line_nobreaks = line.strip()
            # if there's text in the line
            if line_nobreaks != '':
                # if the last character in the line is a punctiation
                if line_nobreaks[-1] in ['.', ';', '!', '?']:
                    # creates a found_text_body variable
                    found_text_body = True

            # if the body of the texts has not started
            if not found_text_body:
                # call function to clean names from line
                # if removing names makes line empty, the line
                # had only names and nothing else
                line_no_names = clean_names_from_line(line)

                # if removing email addresses makes line empty, the line
                # had only email addresses and nothing else
                line_no_emails = clean_email_from_line(line)

                if (line_no_names != '' and
                        line_no_emails != ''):
                    if not ('.' not in line and '<name>' in line):
                        # check if line is a Word comment
                        if not line[0] == '[':
                            # remove other Word comments, e.g., [AP 1]
                            new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', line)
                            # replace emails with <email>
                            new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                            # check if line starts with identifying words
                            matches = re.findall(
                                r'^(professor|prof\.|teacher|instructor|m\.|mrs?\.|ms\.|dr\.|student|net\s?id|id)', new_line2, flags=re.IGNORECASE)
                            # if the line does not start with any of the above
                            if len(matches) == 0:
                                new_line2 = re.sub(r'\s+', r' ', new_line2)
                                output_file.write(new_line2.strip() + '\r\n')


            else:
                # if removing email addresses makes line empty, the line
                # had only email addresses and nothing else
                cleaned_line1 = clean_email_from_line(line)

                # call function to clean names from line
                cleaned_line2 = clean_names_from_line(line)

                if (cleaned_line1 != '' and cleaned_line2 != ''):
                    if not ('.' not in line and '<name>' in line):
                        # check if line is a Word comment
                        if line[0] != '[':
                            new_line2 = re.sub(r'\s+', r' ', line)
                            # remove other Word comments, e.g., [AP 1]
                            new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', new_line2)
                            # replace emails with <email>
                            new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                            output_file.write(new_line2.strip() + '\r\n')

        output_file.close()
        textfile.close()
    return(found_text_files)

def deidentify_recursive(directory, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = deidentify_file(os.path.join(dirpath, name), overwrite)
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')




deidentify_recursive(args.dir)
