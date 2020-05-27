"""
MIT License

Copyright (c) 2020 Phil Niehus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from sys import exit
import argparse
import time
import datetime
from random import randrange
from random import randint
from win32_setctime import setctime
from dateutil.parser import parse as parse_date
from os import path
import os


def main():

    desc = "Sets the creation, modification and access dates of files to a random date in the provided range. Changing the creation dates of directories is not supported."
    epi = "Example: 'Baityfiler.exe 1981-01-01 2012-12-31 test.txt' If the given file is a directory, all files and directories in it will be modified, but not files in subdirectories, the modification and access times of the directory will also be changed."
    parser = argparse.ArgumentParser(prog="Baityfiler - File date randomizer", description=desc, epilog=epi)
    
    parser.add_argument("startdate", help="The beginning of the desired date range. Recommended format: YYYY-MM-DD")
    parser.add_argument("enddate", help="The end of the desired date range")
    parser.add_argument("filepath", help="Path to a file or directory whose creation date(s) should be altered. Recommended format: YYYY-MM-DD")
    parser.add_argument("-r", "--recursive", help="enables recursive processing of sub directories when set", action="store_true")
    
    args = parser.parse_args()
    
    try:
        start = parse_date(args.startdate)
        end = parse_date(args.enddate)
        
        print("Setting dates between ",start, " and ", end, "...")
    except:
        print("INCOMPATIBLE DATE: Recommended date format: YYYY-MM-DD")
        exit(1)
    
    if path.isfile(args.filepath):
        set_file_times(args.filepath, start, end)
        print("Dates successfully changed.")
        exit(0)
    elif path.isdir(args.filepath):
        traverse_directory(args.filepath, start, end, args.recursive)
        print("Dates successfully changed.")
        exit(0)
    else:
        print("Invalid filepath! ( ", args.filepath, " )")
        exit(1)
        
##
# Traverses and modifies dates of directories and contained files
# Dates always follow this format: access > modification > creation
# @param filepath The absolute path to the directory for traversal
# @param first_date The beginning of the date range (datetime object)
# @param last_date The end of the date range (datetime object)
# @param recursive Determines if subdirectories will be visited recursively
def traverse_directory(filepath, first_date, last_date, recursive):
    filepath = path.abspath(filepath)
    dir_date = get_random_date(first_date, last_date)
    set_file_times(filepath, first_date, last_date, dir_date)
    for f in os.listdir(filepath):
        fa = os.path.join(filepath, f)
        if path.isdir(fa) and recursive:
            traverse_directory(fa, dir_date, last_date, recursive)
        else:
            set_file_times(fa, dir_date, last_date)

##
# Modifies the creation , modification and access times of files (modification and access only in case of directories)
# Dates always follow this format: access > modification > creation
# @param filepath The absolute path to the file whose dates should be modified
# @param first_date The beginning of the date range (datetime object)
# @param last_date The end of the date range (datetime object)
# @param creation Optional argument to overwrite the creation date
def set_file_times(filepath, first_date, last_date, creation=None):
    try:
        if creation == None:
            creation = get_random_date(first_date, last_date)
        mod = get_random_date(creation, last_date)
        access = get_random_date(mod, last_date)
        creation_unix = date_time_to_unix_time(creation)
        mod_unix = date_time_to_unix_time(mod)
        access_unix = date_time_to_unix_time(access)
        
        if not path.isdir(filepath):
                setctime(filepath, creation_unix)
        
        
        # To do: make this configurable via param (remember to change param type to int)
        # Mod time is set to creation time 30% of the time for files and 80% of the time for directories
        # Random mod time later then creation time is used otherwise
        rnd = randint(1, 10)
        if rnd  <= 3 or (path.isdir(filepath) and (rnd <= 8)):
            os.utime(filepath, (access_unix, creation_unix))
        else:
            os.utime(filepath, (access_unix, mod_unix))
    except Exception as e:
        print("Failed to modify '", filepath, "' - ", e)
    
##
# Converts datetime objects into unix timestamps    
# @param dt The datetimeobject that will be converted
def date_time_to_unix_time(dt):
    return time.mktime(dt.timetuple())

##
# Generates a random date in the given range   
# @param first_date The beginning of the date range (datetime object)
# @param last_date The end of the date range (datetime object)
# @return A random datetime within the given range
def get_random_date(first_date, last_date):
    difference = last_date - first_date
    random_addition = randrange(difference.total_seconds())
    return first_date + datetime.timedelta(seconds=random_addition)
    
if __name__ == '__main__':
    main()