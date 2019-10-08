#!/usr/bin/env python3

import csv
import json
from os import listdir
from os.path import isfile, join
import datetime


def weightdata(path):
    """
    Given the path to a full-account Fitbit dump,
    load all the weight files and yield the data
    records in them.
    """
    weightfiles = [ join(path, f) for f in listdir(path)
                  if isfile(join(path, f))
                  if f.startswith('weight') ]
    weightfiles.sort()
    for file in weightfiles:
        with open(file, 'r') as f:
            data = json.load(f)
        for d in data:
            yield d


def build_row(data):
    """
    Given a data record from the fitbit weight data dump,
    assemble a row of data suitable for the Withings import
    csv file.
    """
    date = datetime.datetime.strptime('{} {}'.format(data['date'], data['time']), '%m/%d/%y %H:%M:%S')
    weight = data['weight']
    if 'fat' in data:
        fatmass = round(data['fat'] / 100 * data['weight'], 1)
    else:
        fatmass = ''

    return [date, weight, fatmass]


def write_to_file(file_counter, file_data):
    with open('weight_data{}.csv'.format(file_counter), 'w', newline='') as csv_handle:
        writer = csv.writer(csv_handle)
        writer.writerows(file_data)


def init_loop_state(file_counter=0):
    """
    Initialize the file row counter, the file counter,
    and the list representing file data.
    Janky, I know, but this needed to be done in 2 spots.
    """
    file_row_counter = 0
    file_counter += 1

    file_data = []
    file_data.append([
        'Date',
        'Weight (lb)',
        'Fat mass (lb)'
    ])

    return (file_row_counter, file_counter, file_data)

def main():
    user_site_export_path = './JonathanHanson/user-site-export/'

    (file_row_counter, file_counter, file_data) = init_loop_state()

    for data in weightdata(user_site_export_path):
        # Skip any data that fitbit got from withings
        if 'source' in data and data['source'] == 'Withings':
            continue

        file_row_counter += 1

        row = build_row(data)
        file_data.append(row)

        # Withings wants files limited to 300 lines.  Including the
        # column header line, we'll cap at 299 data rows.
        if file_row_counter >=299:
            write_to_file(file_counter, file_data)
            (file_row_counter, file_counter, file_data) = init_loop_state(file_counter)

    write_to_file(file_counter, file_data)


if __name__ == "__main__":
    main()
