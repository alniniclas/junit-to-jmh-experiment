import argparse
import json
import os
import statistics
import math
import itertools
import csv


class BenchmarkExecutionFailedError(Exception):
  pass


def compute_throughput_statistics(throughput_values):
  measurements = len(throughput_values)
  mean = statistics.mean(throughput_values)
  variance = statistics.variance(throughput_values)
  stddev = statistics.stdev(throughput_values)
  stderr = stddev / math.sqrt(measurements)
  cv = stddev / mean
  # Unbiased estimator for normally distributed data.
  cv_est = (1 + (1 / (4 * measurements))) * cv
  return {
    'measurements': measurements,
    'mean': mean,
    'variance': variance,
    'standard_deviation': stddev,
    'standard_error': stderr,
    'cv': cv,
    'cv_est': cv_est
  }


def aggregate_result(result_base_info, throughput_values):
  throughput_stats = compute_throughput_statistics(throughput_values)
  result = dict(result_base_info)
  result.update(throughput_stats)
  return result


def aggregate_results(result_base_info, throughput_values, combine_reps):
  if combine_reps:
    flattened_throughput_values = list(itertools.chain.from_iterable(throughput_values))
    return [aggregate_result(result_base_info, flattened_throughput_values)]
  else:
    results = []
    for repetition in range(len(throughput_values)):
      result = aggregate_result(result_base_info, throughput_values[repetition])
      result['repetition'] = repetition
      results.append(result)
    return results


def get_repetition_dir(class_name, test_name, repetition, config):
  output_dir = os.path.abspath(config['output_dir'])
  return os.path.join(output_dir, class_name, test_name, str(repetition))


def get_unit_test_throughputs(class_name, test_name, config):
  throughputs = []
  for repetition in range(0, config['repetitions']):
    repetition_dir = get_repetition_dir(class_name, test_name, repetition, config)
    results_file = os.path.join(repetition_dir, 'unit-test.json')
    with open(results_file, 'r') as f:
      test_durations = json.load(f)['durations']
    throughputs.append([1.0/float(x) for x in test_durations])
  return throughputs


def get_jmh_throughputs(class_name, test_name, config_name, config):
  throughputs = []
  for repetition in range(0, config['repetitions']):
    repetition_dir = get_repetition_dir(class_name, test_name, repetition, config)
    resunts_file_name = '{}.json'.format(config_name)
    results_file = os.path.join(repetition_dir, resunts_file_name)
    if os.path.getsize(results_file) == 0:
      # An empty results file means that the benchmark execution failed.
      raise BenchmarkExecutionFailedError()
    with open(results_file, 'r') as f:
      raw_throughput = json.load(f)[0]['primaryMetric']['rawData']
    throughputs.append(list(itertools.chain.from_iterable(raw_throughput)))
  return throughputs


def get_unit_test_results(class_name, test_name, config, combine_reps):
  throughput_values = get_unit_test_throughputs(class_name, test_name, config)
  result_base_info = {
    'class': class_name,
    'test': test_name,
    'approach': 'unit-test',
    'unit_test_execution_time': config['junit_time'] / 1000.0,
    'config_name': 'unit-test'
  }
  return aggregate_results(result_base_info, throughput_values, combine_reps)


def get_jmh_results(class_name, test_name, approach_name, jmh_config, config, combine_reps):
  config_name = '{}-f{:d}-t{:d}'.format(approach_name, jmh_config['forks'], jmh_config['time'])
  throughput_values = get_jmh_throughputs(class_name, test_name, config_name, config)
  result_base_info = {
    'class': class_name,
    'test': test_name,
    'approach': approach_name,
    'jmh_forks': jmh_config['forks'],
    'jmh_iteration_time': jmh_config['time'] / 1000.0,
    'config_name': config_name
  }
  return aggregate_results(result_base_info, throughput_values, combine_reps)


def get_test_case_results(class_name, test_name, config, combine_reps):
  results = []
  results.extend(get_unit_test_results(class_name, test_name, config, combine_reps))
  for approach_name in 'ju2jmh', 'ju4runner':
    for jmh_config in config['jmh_configs']:
      results.extend(get_jmh_results(class_name, test_name, approach_name, jmh_config, config, combine_reps))
  return results


def get_csv_field_names(combine_reps):
  return [
    'class',
    'test',
    'approach',
    'unit_test_execution_time',
    'jmh_forks',
    'jmh_iteration_time',
    'config_name'
  ] + (['repetition'] if not combine_reps else []) + [
    'measurements',
    'mean',
    'variance',
    'standard_deviation',
    'standard_error',
    'cv',
    'cv_est'
  ]


def write_output_file_headers(output_file, combine_reps):
  csv_field_names = get_csv_field_names(combine_reps)
  with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, csv_field_names, dialect=csv.unix_dialect)
    csv_writer.writeheader()


def write_results_batch(output_file, results_batch, combine_reps):
  csv_field_names = get_csv_field_names(combine_reps)
  with open(output_file, 'a') as f:
    csv_writer = csv.DictWriter(f, csv_field_names, dialect=csv.unix_dialect)
    csv_writer.writerows(results_batch)


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
  
  with open(args.config, 'r') as f:
    config = json.load(f)
  output_dir = os.path.abspath(config['output_dir'])
  progress_file = os.path.join(output_dir, 'progress.json')
  with open(progress_file, 'r') as f:
    last_test_index = json.load(f)['test_index']
  with open(config['test_list'], 'r') as f:
    tests = json.load(f)[:last_test_index + 1]
  output_file = args.output_file if args.output_file else os.path.join(output_dir, 'results.csv')

  write_output_file_headers(output_file, args.combine_reps)
  results_batch = []
  for i in range(len(tests)):
    if len(results_batch) > 1000:
      write_results_batch(output_file, results_batch, args.combine_reps)
      results_batch = []

    test = tests[i]
    print('[{:d}/{:d}] {}.{}'.format(i + 1, len(tests), test['class'], test['test']))
    try:
      results_batch.extend(get_test_case_results(test['class'], test['test'], config, args.combine_reps))
      clear_console_line()
    except BenchmarkExecutionFailedError:
      clear_console_line()
      print('[{:d}/{:d}] Skipping {}.{} due to one or more failed JMH executions.'.format(i + 1, len(tests), test['class'], test['test']))
  write_results_batch(output_file, results_batch, args.combine_reps)
  print('Done. Results written to {}'.format(output_file))


if __name__ == '__main__':
  main()
