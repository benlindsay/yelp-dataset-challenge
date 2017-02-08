"""
Helper functions for Yelp dataset challenge
"""
import json
import csv
import string
import sys
import re

def load_json_lines(fname):
  """Yields the JSON data in fname, which should have one JSON object per line"""
  with open(fname) as f:
    for line in f:
      yield json.loads(line)

def convert_data_file(json_file_name, output, max_files = int(5e25)):
    """
    Converts the provided json files to sepparate CSV files in the output folder, call it with:
    convert_data_file('../raw-data/yelp_academic_dataset_review.json', '../raw-data/reviews/file-')
    and it will all files into the reviews folder: reviews/file-1.csv, reviews/file-2.csv, etc
    """
    file_index = 0
    with open(json_file_name, 'r') as json_input: 
        for line in json_input:
            json_line = json.loads(line)

            file_index += 1
            if file_index > max_files: break
            with open(output + str(file_index) + '.csv', 'w') as csv_output:
                csv_writer = csv.writer(csv_output)
                
                csv_writer.writerow(json_line.keys())
                csv_writer.writerow(json_line.values())
                

def create_single_csv(json_file_name, output, exclude=[], max_lines = False):
    """
    converts the entered JSON file into a single CSV, excluding the rows whose indexes appear in exclude
    max - is the maximum number of lines to be processed
    """
    regex = re.compile('[^\w\ \'.,]')
    
    header = False
    with open(output, 'w') as csv_output:
        csv_writer = csv.writer(csv_output)
        x = 0
        for json_line in load_json_lines(json_file_name):
            x += 1
            if x in exclude: continue
            if max_lines and x > max_lines: break

            if not header:
                header = json_line.keys()
                csv_writer.writerow(header)

            # there're characters in the text that cause issues with the generated CSV, remove them
            json_line['text'] = regex.sub('', json_line['text'])
            csv_writer.writerow(json_line.values())

