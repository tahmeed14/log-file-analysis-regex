# -*- coding: utf-8 -*-
#!/usr/bin/python -tt

## Name: Tahmeed Tureen
## SI 330 -- Data Manipulation -- HW4
## Dr. Teplovs -- Fall 2017

import re
import csv
from collections import defaultdict


def write_log_entries(filename, list_of_rows_to_write):
    row_counter = 0
    with open(filename, 'w+', newline = '') as f:
        row_writer = csv.DictWriter(f, delimiter='\t', quotechar='"', extrasaction='ignore',
                                    fieldnames=["IP", "Ignore1", "Ignore2", "Timestamp", "Ignore3", "HTTP_Verb",
                                                "HTTP_Status", "HTTP_Duration", "HTTP_Redirect", "Browser_Type",
                                                "Top_Level_Domain"])
        row_writer.writeheader()
        for row in list_of_rows_to_write:
            top_level = get_toplevel_domain(row["HTTP_Verb"])
            row["Top_Level_Domain"] = top_level

            row_writer.writerow(row)
            row_counter = row_counter + 1

    print("Wrote {} rows to {}".format(row_counter, filename))

# Function get_top-level_domain:
#    Input:  A string containing a URL
#    Output:  the top-level domain in the URL, or None if no valid top-level domain was found.  The top-level
#             domain, if it exists, should be normalized to always be in lower case.

def get_toplevel_domain(url):
    ### Use re.search here with the appropriate regular expression to look for a match
    ### Hint: define a group to pull out the top-level domain from the match
    #match = re.search(r'^(GET|POST)\s+(http:\/\/|https:\/\/)[A-z-]+[\w.-]*.[.]([a-zA-Z]{2,5})(?:\/{1}|\:{1})?', url)
    # Looks like the top level domain length ranges from 2 to 5 letters in the desired output
    #^(GET|POST)\s+(http:\/\/|http:\/\/)[A-z]+[\w.]+.+[.]([a-zA-Z]{2,3})[\/]
    #^(GET|POST)\s+(http:\/\/|http:\/\/)[A-z]+[\w.]+.+[.]([a-zA-Z]{2,3})(?:\/{1}|\:{1})

    if get_url_starter(url) == True:
        match = re.search(r'^(GET|POST)\s+(http:\/\/|https:\/\/)[A-z-]+[\w.-]*[.]([a-zA-Z]{2,})(?:\/{1}|\:{1})?', url)
    
    # Note that some of the invalid urls still have top level domains
    else:
         match = re.search(r'(http:\/\/|https:\/\/)([A-z-]+[\w.-]*[.])([a-zA-Z]{2,})(?:\/{1}|\:{1})?', url)
    #([\w+.]+[.])

    if match == None: # There is only one group here
        return None

    match_lower = match.group(3).lower()
    return match_lower

# Function get_status_success:
# This function will check the status code of a log request
# If the status is not 200 then it is INVALID. Otherwise VALID
# Used in main()

def get_status_success(status):
    match = re.search(r'200', status)
    if match == None: # If match is not found, return None
        return None

    return True

# Function get_GET_POST:
# This function will check if a log request has GET or POST in the request
# If GET or POST exists, then the request is VALID. OTHERWISE

def get_GET_POST(url):
    match = re.search(r'^(GET|POST)\s+', url)
    if match == None:
        return None

    # GET or POST exists, so return True
    return True

# Function will check if the url has atleast 1 character (NOT A digit after https:// or http://)
# If so, will return True
def get_url_starter(url):
    match = re.search(r'^(GET|POST)\s+(https:\/\/|http:\/\/)[a-zA-Z]+', url)
    if match == None:
        return None

    return True

# Function read_log_file:
#   Input: the file name of the log file to process
#   Output:  A two-element tuple with element 0 a list of valid rows, and element 1 a list of invalid rows
def read_log_file(filename):
    valid_entries   = []
    invalid_entries = []

    with open(filename, 'r', newline='') as input_file:
        log_data_reader = csv.DictReader(input_file, delimiter='\t', quotechar ='"', skipinitialspace=True,
                                         fieldnames=["IP","Ignore1","Ignore2","Timestamp","Ignore3","HTTP_Verb","HTTP_Status","HTTP_Duration","HTTP_Redirect","Browser_Type"])
        for row in log_data_reader:
            not_a_valid_line = False

            ### PUT YOUR CODE HERE to test for a valid line and set not_a_valid_line to True if a condition isn't met

            #url_GETPOST = get_GET_POST(row["HTTP_Verb"])
            success_code = get_status_success(row["HTTP_Status"])
            url_starter = get_url_starter(row["HTTP_Verb"])
            toplevel_domain = get_toplevel_domain(row["HTTP_Verb"])

            # Check conditions for valid line:
            # If one condition breaks, the the line is NOT VALID

            if (success_code == None or url_starter == None or toplevel_domain == None):
                not_a_valid_line = True


            if not_a_valid_line: # If true
                invalid_entries.append(row)
                continue

            # If we get here, it's a valid line
            valid_entries.append(row)


    return (valid_entries, invalid_entries)

def main():
    #valid_rows, invalid_rows = read_log_file(r'access_log.txt')
    #valid_rows, invalid_rows = read_log_file('access_log_first_1000_lines.txt')
    valid_rows, invalid_rows = read_log_file('access_log.txt')

    write_log_entries('valid_access_log_TUREEN.txt', valid_rows)
    write_log_entries('invalid_access_log_TUREEN.txt', invalid_rows)

# This is boilerplate python code: it tells the interpreter to execute main() only
# if this module is being run as the main script by the interpreter, and
# not being imported as a module.
if __name__ == '__main__':
    main()

