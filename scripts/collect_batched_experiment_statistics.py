import argparse
import batched_experiment.config
import batched_experiment.statistics_collector
import csv
import os


def write_headers(fields, output_file):
  with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
    csv_writer.writeheader()


def write_rows(fields, rows, output_file):
  with open(output_file, 'a') as f:
    csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
    csv_writer.writerows(rows)


def row_dict(statistics, test, runner_config, batch, repetition=None):
  row = {
    'class': test.class_name,
    'test': test.method_name,
    'config_name': runner_config.name,
    'approach': runner_config.approach,
    'batch': batch,
    'error': ','.join(sorted(set(statistics.result.errors))),
    'measurements': statistics.measurements,
    'mean': statistics.mean,
    'variance': statistics.variance,
    'standard_deviation': statistics.stddev,
    'standard_error': statistics.stderr,
    'cv': statistics.cv,
    'cv_est': statistics.cv_est
  }
  if repetition is not None:
    row['repetition'] = repetition
  return row


def clear_console_line():
  print('\033[F\033[K', end='')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  parser.add_argument('--combine-repetitions', dest='combine_reps',
                      action='store_true')
  parser.add_argument('--output-file', type=str)
  parser.set_defaults(combine_reps=False)
  args = parser.parse_args()

  config = batched_experiment.config.BatchedExperimentConfiguration.parse_from_file(args.config)
  
  output_file = args.output_file if args.output_file else os.path.join(config.output_dir, 'statistics.csv')
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

  write_headers(field_names, output_file)

  statistics_collector = batched_experiment.statistics_collector.StatisticsCollector(config)

  for batch in range(statistics_collector.finished_batches):
    print('batch {:d}/{:d}'.format(batch + 1, statistics_collector.finished_batches))
    batch_statistics = statistics_collector.collect_batch_statistics(batch, combine_repetitions=args.combine_reps)
    rows = []
    for test in config.test_batches[batch]:
      for runner_config in config.runner_configs:
        if args.combine_reps:
          rows.append(row_dict(batch_statistics[test, runner_config], test, runner_config, batch))
        else:
          for repetition in range(statistics_collector.repetitions):
            rows.append(row_dict(
              batch_statistics[test, runner_config, repetition], test, runner_config, batch, repetition
            ))
    write_rows(field_names, rows, output_file)
    clear_console_line()


if __name__ == '__main__':
  main()
