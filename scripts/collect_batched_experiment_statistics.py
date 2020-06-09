import argparse
import csv
import os
import pickle


from batched_experiment.experiment_statistics import ThroughputStatistics


def clear_console_line():
  print('\033[F\033[K', end='')


def row_dict(result, statistics):
  row = {
    'class': result.test.class_name,
    'test': result.test.method_name,
    'config_name': result.runner.name,
    'approach': result.runner.approach,
    'batch': result.batch,
    'error': ','.join(sorted(set(statistics.result.errors))),
    'measurements': statistics.measurements,
    'mean': statistics.mean,
    'variance': statistics.variance,
    'standard_deviation': statistics.stddev,
    'standard_error': statistics.stderr,
    'cv': statistics.cv,
    'cv_est': statistics.cv_est
  }
  if result.repetition is not None:
    row['repetition'] = result.repetition
  return row


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('data_file', type=str)
  parser.add_argument('output_file', type=str)
  parser.add_argument('--combine-repetitions', dest='combine_reps',
                      action='store_true')
  parser.set_defaults(combine_reps=False)
  args = parser.parse_args()

  with open(args.data_file, 'rb') as f:
    data = pickle.load(f)

  field_names = [
    'class',
    'test',
    'config_name',
    'approach',
    'batch'
  ] + (['repetition'] if not args.combine_reps else []) + [
    'error',
    'measurements',
    'mean',
    'variance',
    'standard_deviation',
    'standard_error',
    'cv',
    'cv_est'
  ]
  
  with open(args.output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, field_names, dialect=csv.unix_dialect)
    csv_writer.writeheader()

  for batch in range(len(data.config.test_batches)):
    rows = []
    print('processing batch {:d}/{:d}'.format(batch + 1, len(data.config.test_batches)))
    for result in data.get_results(batch=batch, combine_repetitions=args.combine_reps):
      rows.append(row_dict(result, ThroughputStatistics(result.result)))
    with open(args.output_file, 'a') as f:
      csv_writer = csv.DictWriter(f, field_names, dialect=csv.unix_dialect)
      csv_writer.writerows(rows)
    clear_console_line()


if __name__ == '__main__':
  main()
