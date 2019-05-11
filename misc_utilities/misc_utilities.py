#!/usr/bin/python

"""

Misc. Utilities

Owner : paul-tqh-nguyen

Created : 05/11/2019

File Organization:
* Printing Utilities

"""

#######################
# Printing Utilities #
#######################

def p1(iterable, number_of_newlines=1):
    number_of_necessary_additional_newlines = (number_of_newlines - 1)
    for element in iterable:
        element_string = str(element)
        additional_new_lines = ("\n"*number_of_necessary_additional_newlines)
        print(element_string+additional_new_lines)
