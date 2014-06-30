#!/usr/bin/env python

import ucsv, sys, argparse

# Command-line argument: specify the CSV data file
parser = argparse.ArgumentParser(description='Specify the Capsule CSV backup to check for duplicates.')
parser.add_argument('csv', help='the CapsuleCRM CSV data file to import')
args = parser.parse_args()

try:
    reader = ucsv.UnicodeDictReader(open(args.csv))
except IOError:
    print "Could not read the specified CSV data file: %S" % args.csv
    sys.exit()

rows = list(reader)
total_rows = len(rows)




### WORK IN PROGRESS: this is a script to discover and flag potential duplicates in Capsule
