import argparse
import batched_experiment.config
import batched_experiment.data_collector
import batched_experiment.statistics_collector
import csv
import json
import os
import scipy.stats


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
    baseline = batched_experiment.config.Test(test_pair_dict['baseline']['class'], test_pair_dict['baseline']['test'])
    slowdown = batched_experiment.config.Test(test_pair_dict['slowdown']['class'], test_pair_dict['slowdown']['test'])
    return TestPair(baseline, slowdown)


def write_headers(fields, output_file):
  with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
    csv_writer.writeheader()


def write_rows(fields, rows, output_file):
  with open(output_file, 'a') as f:
    csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
    csv_writer.writerows(rows)


def row_dict(baseline_statistics, slowdown_statistics, test_result, test_pair, runner_config, batch, repetition=None):
  row = {
    'baseline_class': test_pair.baseline.class_name,
    'baseline_test': test_pair.baseline.method_name,
    'slowdown_class': test_pair.slowdown.class_name,
    'slowdown_test': test_pair.slowdown.method_name,
    'config_name': runner_config.name,
    'approach': runner_config.approach,
    'batch': batch,
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
  if repetition is not None:
    row['repetition'] = repetition
  return row

def clear_console_line():
  print('\033[F\033[K', end='')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  parser.add_argument('test_pairs', type=str)
  parser.add_argument('--combine-repetitions', dest='combine_reps',
                      action='store_true')
  parser.add_argument('--output-file', type=str)
  parser.set_defaults(combine_reps=False)
  args = parser.parse_args()

  config = batched_experiment.config.BatchedExperimentConfiguration.parse_from_file(args.config)

  with open(args.test_pairs, 'r') as f:
    test_pairs = [TestPair.parse_from_dict(tpd) for tpd in json.load(f)]
  test_pair_dict = {}
  for test_pair in test_pairs:
    if test_pair.baseline not in test_pair_dict:
      test_pair_dict[test_pair.baseline] = []
    test_pair_dict[test_pair.baseline].append(test_pair)

  output_file = args.output_file if args.output_file else os.path.join(config.output_dir, 'slowdown-tests.csv')
  field_names = [
    'baseline_class',
    'baseline_test',
    'slowdown_class',
    'slowdown_test',
    'config_name',
    'approach',
    'batch'
  ] + (['repetition'] if not args.combine_reps else []) + [
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

  write_headers(field_names, output_file)

  data_collector = batched_experiment.data_collector.ExperimentDataCollector(config)

  for batch in range(data_collector.finished_batches):
    print('batch {:d}/{:d}'.format(batch + 1, data_collector.finished_batches))
    batch_data = data_collector.collect_batch_data(batch, combine_repetitions=args.combine_reps)
    result_rows = {}
    for baseline, runner_config, *maybe_repetition in batch_data:
      if baseline not in test_pair_dict:
        continue
      for test_pair in test_pair_dict[baseline]:
        baseline_result = batch_data[(baseline, runner_config, *maybe_repetition)]
        slowdown_result = batch_data[(test_pair.slowdown, runner_config, *maybe_repetition)]
        baseline_statistics = batched_experiment.statistics_collector.ThroughputStatistics(baseline_result)
        slowdown_statistics = batched_experiment.statistics_collector.ThroughputStatistics(slowdown_result)
        test_result = scipy.stats.mannwhitneyu(
          baseline_result.throughput, slowdown_result.throughput, use_continuity=False, alternative='greater'
        ) if not baseline_result.errors and not slowdown_result.errors else None
        if test_pair not in result_rows:
          result_rows[test_pair] = {}
        result_rows[test_pair][(runner_config, *maybe_repetition)] = row_dict(
          baseline_statistics, slowdown_statistics, test_result, test_pair, runner_config, batch, *maybe_repetition
        )
    rows = []
    for test_pair in test_pairs:
      if test_pair in result_rows:
        for runner_config in config.runner_configs:
          if args.combine_reps:
            rows.append(result_rows[test_pair][(runner_config,)])
          else:
            for repetition in range(config.repetitions):
              rows.append(result_rows[test_pair][runner_config, repetition])
    write_rows(field_names, rows, output_file)
    clear_console_line()


if __name__ == '__main__':
  main()
