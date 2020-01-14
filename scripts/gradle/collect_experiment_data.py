import argparse
import json
import os
import statistics
import math
import itertools
import csv


def throughput_statistics(throughput_values):
  measurements = len(throughput_values)
  mean = statistics.mean(throughput_values)
  variance = statistics.variance(throughput_values)
  stddev = statistics.stdev(throughput_values)
  stderr = stddev / math.sqrt(measurements)
  # Unbiased estimator for normally distributed data.
  cv = (1 + (1 / (4 * measurements))) * (stddev / mean)
  return {
    'measurements': measurements,
    'mean': mean,
    'variance': variance,
    'standard_deviation': stddev,
    'standard_error': stderr,
    'coefficient_of_variation_est': cv
  }


def get_test_case_results(class_name, test_name, config):
  output_dir = os.path.abspath(config['output_dir'])
  test_case_dir = os.path.join(output_dir, class_name, test_name)
  results = []
  for repetition in range(0, config['repetitions']):
    repetition_dir = os.path.join(test_case_dir, str(repetition))
    with open(os.path.join(repetition_dir, 'unit-test.json'), 'r') as f:
      unit_test_runtimes = json.load(f)['durations']
    unit_test_throughput = [1.0/float(x) for x in unit_test_runtimes]
    unit_test_result = {
      'class': class_name,
      'test': test_name,
      'repetition': repetition,
      'approach': 'unit-test',
      'unit_test_execution_time': config['junit_time'] / 1000.0
    }
    unit_test_result.update(throughput_statistics(unit_test_throughput))
    results.append(unit_test_result)
    for jmh_config in config['jmh_configs']:
      file_name = 'ju2jmh-f{:d}-t{:d}.json'.format(jmh_config['forks'], jmh_config['time'])
      results_file = os.path.join(repetition_dir, file_name)
      if os.path.getsize(results_file) == 0:
        # Benchmark execution failed. Ignore this test case.
        return []
      with open(results_file, 'r') as f:
        ju2jmh_raw_throughput = json.load(f)[0]['primaryMetric']['rawData']
      ju2jmh_throughput = list(itertools.chain.from_iterable(ju2jmh_raw_throughput))
      ju2jmh_result = {
        'class': class_name,
        'test': test_name,
        'repetition': repetition,
        'approach': 'ju2jmh',
        'jmh_forks': jmh_config['forks'],
        'jmh_iteration_time': jmh_config['time'] / 1000.0
      }
      ju2jmh_result.update(throughput_statistics(ju2jmh_throughput))
      results.append(ju2jmh_result)
    for jmh_config in config['jmh_configs']:
      file_name = 'ju4runner-f{:d}-t{:d}.json'.format(jmh_config['forks'], jmh_config['time'])
      with open(os.path.join(repetition_dir, file_name), 'r') as f:
        ju4runner_raw_throughput = json.load(f)[0]['primaryMetric']['rawData']
      ju4runner_throughput = list(itertools.chain.from_iterable(ju4runner_raw_throughput))
      ju4runner_result = {
        'class': class_name,
        'test': test_name,
        'repetition': repetition,
        'approach': 'ju4runner',
        'jmh_forks': jmh_config['forks'],
        'jmh_iteration_time': jmh_config['time'] / 1000.0
      }
      ju4runner_result.update(throughput_statistics(ju4runner_throughput))
      results.append(ju4runner_result)
  return results


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  args = parser.parse_args()
  
  with open(args.config, 'r') as f:
    config = json.load(f)

  output_dir = os.path.abspath(config['output_dir'])
  progress_file = os.path.join(output_dir, 'progress.json')
  with open(progress_file, 'r') as f:
    last_test_index = json.load(f)['test_index']
  with open(config['test_list'], 'r') as f:
    tests = json.load(f)[:last_test_index + 1]
  results = []
  for test in tests:
    print('Reading output for {}.{}'.format(test['class'], test['test']))
    results.extend(get_test_case_results(test['class'], test['test'], config))
  output_file = os.path.join(output_dir, 'results.csv')
  csv_field_names = [
    'class',
    'test',
    'approach',
    'unit_test_execution_time',
    'jmh_forks',
    'jmh_iteration_time',
    'repetition',
    'measurements',
    'mean',
    'variance',
    'standard_deviation',
    'standard_error',
    'coefficient_of_variation_est'
  ]
  with open(output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, csv_field_names, dialect=csv.unix_dialect)
    csv_writer.writeheader()
    csv_writer.writerows(results)


if __name__ == '__main__':
  main()
