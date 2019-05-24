#!/usr/bin/python

"""

PDF Scraping Utilities

Owner : paul-tqh-nguyen

Created : 05/01/2019

File Organization:
* PDF to CSV Utilities

"""

import os
import ntpath
import tabula
from misc_utilities import *

########################
# PDF to CSV Utilities #
########################

def convert_all_pdfs_to_csvs(input_directory, output_directory):
    '''@param 0 INPUT_DIRECTORY ; a text string corresponding to the input directory
       @param 1 OUTPUT_DIRECTORY ; a text string corresponding to the output directory
       @return success status
       Takes an input directory INPUT_DIRECTORY, finds all PDFs, tries to convert them to CSVs, and puts them in OUTPUT_DIRECTORY. Ignores errors and keeps going.
       The location where the CSVs are placed in the output directory will match (wrt nested directory structures) that of the input PDF file.
       For example, if INPUT_DIRECTORY is /input/ and OUTPUT_DIRECTORY is /output/ and we are converting the file /input/first/second/file.pdf, the converted CSV 
       will be /input/first/second/file.csv
       @return success status'''
    assert os.path.isdir(input_directory), "The input directory {0} does not currently exist.".format(input_directory)
    assert os.path.isdir(output_directory), "The output directory {0} does not currently exist.".format(output_directory)
    pdf_file_locations = all_files_with_extension(input_directory,"pdf")
    for pdf_file_location in pdf_file_locations:
        pdf_file_location_relative_to_input_directory = os.path.relpath(pdf_file_location, input_directory)
        output_csv_file_name_without_path_and_without_extension = file_location_strip_extension_and_path(pdf_file_location_relative_to_input_directory)
        output_csv_file_name_without_path = output_csv_file_name_without_path_and_without_extension + ".csv" # @todo do something cleaner
        destination_directory_relative_to_output_directory = os.path.dirname(pdf_file_location_relative_to_input_directory)
        destination_directory = os.path.join(output_directory, destination_directory_relative_to_output_directory)
        if not os.path.isdir(destination_directory):
            os.makedirs(destination_directory)
        output_csv_file_name = os.path.join(destination_directory, output_csv_file_name_without_path)
        pdf_to_csv(pdf_file_location, output_csv_file_name)
    return True

def pdf_to_csv(input_pdf_location, output_csv_location):
    '''@param 0 INPUT_PDF_LOCATION ; a text string corresponding to the location of some PDF on the file system
       @param 1 OUTPUT_CSV_LOCATION ; a text string corresponding to the location of the desired CSV file
       @return success status'''
    assert file_has_extension(input_pdf_location, ".pdf"), "{0} is not a PDF.".format(input_pdf_location)
    assert os.path.isfile(input_pdf_location), "{0} does not exist.".format(input_pdf_location)
    assert file_has_extension(output_csv_location, ".csv"), "{0} does not specify a CSV.".format(output_csv_location)
    tabula.convert_into(input_pdf_location, output_csv_location, output_format="csv", pages='all')
    return True

# helpers

def file_has_extension(file_location, extension_0):
    '''@param 0 FILE_LOCATION ; the path to the file in question
       @param 1 EXTENSION_0 ; the desired extension we want for FILE_LOCATION, e.g. "csv" or ".csv" ; this input is dwimmed to include the preceding "." if it is not included
       @return sucecss status
       Checks if FILE_LOCATION has the extension specified by EXTENSION_0'''
    assert isinstance(file_location, str), "{0} is not a string.".format(file_location)
    assert isinstance(extension_0, str), "{0} is not a string.".format(extension_0)
    extension = dwim_file_extension(extension_0)
    file_location_lowercase = file_location.lower()
    file_has_extension_p = file_location_lowercase.endswith(extension)
    return file_has_extension_p

def file_location_strip_extension_and_path(file_location):
    '''@param 0 FILE_LOCATION ; the path to the file in question
       @return just the file name without the path leading up to it and without the extension.
       E.g. "/home/our_fav_user/diary.txt" => "diary"'''
    file_name_without_path = ntpath.basename(file_location)
    file_name_without_path_and_without_extension = os.path.splitext(file_name_without_path)[0]
    return file_name_without_path_and_without_extension

def dwim_file_extension(extension_0):
    '''@param 0 EXTENSION_0 ; the original input string that we want to DWIM
       @return canonical extension of the form ".<lower-case-extension>" '''
    assert isinstance(extension_0, str), "{0} is not a string.".format(extension_0)
    extension_starts_with_period_p = (extension_0[0] == ".")
    if extension_starts_with_period_p:
        extension = extension_0
    else:
        extension = "." + extension_0
    extension = extension.lower()
    return extension

def all_files_with_extension(input_directory, extension):
    '''@param 0 INPUT_DIRECTORY ; a text string corresponding to the input directory
       @param 1 EXTENSION ; the extension that desired files will have
       @return list of absolute file paths within INPUT_DIRECTORY that have extension EXTENSION'''
    input_directory_absolute = os.path.abspath(input_directory)
    result = list()
    for root_directory, directories, files in os.walk(input_directory_absolute):
        for file in files:
            if file_has_extension(file, extension):
                result.append(os.path.join(root_directory, file))
    return result
