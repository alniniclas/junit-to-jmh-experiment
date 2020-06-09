import argparse
import csv
import json
import pickle
import scipy.stats


from batched_experiment.config import Test
from batched_experiment.experiment_statistics import ThroughputStatistics


class TestPair:
  def __init__(self, baseline, slowdown):
    self.baseline = baseline
    self.slowdown = slowdown

  def __eq__(self, other):
    if isinstance(other, TestPair):
      return (self.baseline, self.slowdown) == (other.baseline, other.slowdown)
    return NotImplemented

  def __hash__(self):
    return hash((self.baseline, self.slowdown))

  @staticmethod
  def parse_from_dict(test_pair_dict):
    baseline = Test(test_pair_dict['baseline']['class'], test_pair_dict['baseline']['test'])
    slowdown = Test(test_pair_dict['slowdown']['class'], test_pair_dict['slowdown']['test'])
    return TestPair(baseline, slowdown)


def write_headers(fields, output_file):
  with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
    csv_writer.writeheader()


def write_rows(fields, rows, output_file):
  with open(output_file, 'a') as f:
    csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
    csv_writer.writerows(rows)


def row_dict(baseline, slowdown, baseline_statistics, slowdown_statistics, test_result):
  row = {
    'baseline_class': baseline.test.class_name,
    'baseline_test': baseline.test.method_name,
    'slowdown_class': slowdown.test.class_name,
    'slowdown_test': slowdown.test.method_name,
    'config_name': baseline.runner.name,
    'approach': baseline.runner.approach,
    'baseline_batch': baseline.batch,
    'slowdown_batch': slowdown.batch,
    'baseline_error': ','.join(sorted(set(baseline_statistics.result.errors))),
    'slowdown_error': ','.join(sorted(set(slowdown_statistics.result.errors))),
    'baseline_measurements': baseline_statistics.measurements,
    'slowdown_measurements': slowdown_statistics.measurements,
    'baseline_mean': baseline_statistics.mean,
    'slowdown_mean': slowdown_statistics.mean,
    'mean_delta': (
      slowdown_statistics.mean - baseline_statistics.mean
      if baseline_statistics.mean and slowdown_statistics.mean else None
    ),
    'baseline_standard_deviation': baseline_statistics.stddev,
    'slowdown_standard_deviation': slowdown_statistics.stddev,
    'statistic': test_result.statistic if test_result else None,
    'p_value': test_result.pvalue if test_result else None
  }
  if baseline.repetition is not None:
    row['baseline_repetition'] = baseline.repetition
  if slowdown.repetition is not None:
    row['slowdown_repetition'] = slowdown.repetition
  return row


def clear_console_line():
  print('\033[F\033[K', end='')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('data_file', type=str)
  parser.add_argument('test_pairs', type=str)
  parser.add_argument('output_file', type=str)
  parser.add_argument('--combine-repetitions', dest='combine_reps',
                      action='store_true')
  parser.set_defaults(combine_reps=False)
  args = parser.parse_args()

  with open(args.data_file, 'rb') as f:
    data = pickle.load(f)

  with open(args.test_pairs, 'r') as f:
    test_pairs = [TestPair.parse_from_dict(tpd) for tpd in json.load(f)]

  field_names = [
    'baseline_class',
    'baseline_test',
    'slowdown_class',
    'slowdown_test',
    'config_name',
    'approach',
    'baseline_batch'
  ] + (['baseline_repetition'] if not args.combine_reps else []) + [
    'slowdown_batch'
  ] + (['slowdown_repetition'] if not args.combine_reps else []) + [
    'baseline_error',
    'slowdown_error',
    'baseline_measurements',
    'slowdown_measurements',
    'baseline_mean',
    'slowdown_mean',
    'mean_delta',
    'baseline_standard_deviation',
    'slowdown_standard_deviation',
    'statistic',
    'p_value'
  ]

  write_headers(field_names, args.output_file)

  rows = []
  for tp in range(len(test_pairs)):
    print('processing pair {:d}/{:d}'.format(tp + 1, len(test_pairs)))
    test_pair = test_pairs[tp]
    for runner in data.config.runner_configs:
      baselines = data.get_results(test=test_pair.baseline, runner=runner, combine_repetitions=args.combine_reps)
      slowdowns = data.get_results(test=test_pair.slowdown, runner=runner, combine_repetitions=args.combine_reps)
      for baseline, slowdown in zip(baselines, slowdowns):
        test_result = scipy.stats.mannwhitneyu(
          baseline.result.throughput, slowdown.result.throughput, use_continuity=False, alternative='greater'
        ) if not baseline.result.errors and not slowdown.result.errors else None
        rows.append(row_dict(
          baseline, slowdown, ThroughputStatistics(baseline.result), ThroughputStatistics(slowdown.result), test_result
        ))
    if len(rows) >= 1000:
      write_rows(field_names, rows, args.output_file)
      rows = []
    clear_console_line()
  if rows:
    write_rows(field_names, rows, args.output_file)


if __name__ == '__main__':
  main()
