import argparse
import os
import csv


def read_input(input_file):
  with open(input_file, 'r') as f:
    reader = csv.DictReader(f, dialect=csv.unix_dialect)
    return [row for row in reader]


def get_output_key(row):
  test_class = row['class']
  test_name = row['test']
  if 'repetition' not in row:
    return test_class, test_name
  else:
    return test_class, test_name, row['repetition']


def write_output(output_file, column_names, rows):
  with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, column_names, dialect=csv.unix_dialect)
    csv_writer.writeheader()
    csv_writer.writerows(rows)
    

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input_file', type=str)
  parser.add_argument('output_file', type=str)
  parser.add_argument('column', type=str, choices={
    'measurements', 'mean', 'variance', 'standard_deviation', 'standard_error', 'cv', 'cv_est'
  })
  args = parser.parse_args()

  output_dict = {}
  output_rows = []
  has_repetitions = False
  config_names = []
  for row in read_input(args.input_file):
    key = get_output_key(row)
    if key not in output_dict:
      output_dict[key] = {
        'class': row['class'],
        'test': row['test']
      }
      if 'repetition' in row:
        has_repetitions = True
        output_dict[key]['repetition'] = row['repetition']
      output_rows.append(output_dict[key])
    if row['config_name'] not in config_names:
      config_names.append(row['config_name'])
    output_dict[key][row['config_name']] = row[args.column]
  output_column_names = ['class', 'test'] + (['repetition'] if has_repetitions else []) + config_names
  write_output(args.output_file, output_column_names, output_rows)


if __name__ == '__main__':
  main()
