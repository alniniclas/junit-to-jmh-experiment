import argparse
import json
import os
import statistics
import math
import itertools
import csv


class BenchmarkExecutionFailedError(Exception):
  pass


def clear_console_line():
  print('\033[F\033[K', end='')


class GradleTestDataCollector:
  def __init__(self, name):
    self.name = name
    self.approach = 'gradle-test'

  def collect_batch_data(self, tests, batch_output_dir):
    batch_output_file = os.path.join(batch_output_dir, '{}_output.json'.format(self.name))
    with open(batch_output_file, 'r') as f:
      batch_output = json.load(f)
    test_durations = {(t['class'], t['test']): t['test_durations'] for t in batch_output}
    results = []
    for test in tests:
      result = {}
      try:
        result['throughput'] = self.durations_to_throughput(test_durations[test['class'], test['test']])
      except BenchmarkExecutionFailedError:
        result['error'] = 'FAILED'
      except ZeroDivisionError:
        result['error'] = 'ZERO_DURATION'
      results.append(result)
    return results

  def durations_to_throughput(self, durations):
    for duration in durations:
      if duration == 'FAILED':
        raise BenchmarkExecutionFailedError()
    return [1.0 / float(d) for d in durations]


class JmhBenchmarkDataCollector:
  def __init__(self, name, approach):
    self.name = name
    self.approach = approach

  def collect_batch_data(self, tests, batch_output_dir):
    runner_output_dir = os.path.join(batch_output_dir, self.name)
    results = []
    for test in tests:
      result = {}
      try:
        result['throughput'] = self.collect_benchmark_data(test['class'], test['test'], runner_output_dir)
      except BenchmarkExecutionFailedError:
        result['error'] = 'FAILED'
      results.append(result)
    return results

  def collect_benchmark_data(self, class_name, test_name, runner_output_dir):
    benchmark_output_dir = os.path.join(runner_output_dir, class_name, test_name)
    benchmark_output_file = os.path.join(benchmark_output_dir, 'output.json')
    if os.path.getsize(benchmark_output_file) == 0:
      # An empty results file means that the benchmark execution failed.
      raise BenchmarkExecutionFailedError()
    with open(benchmark_output_file, 'r') as f:
      raw_throughput = json.load(f)[0]['primaryMetric']['rawData']
    return list(itertools.chain.from_iterable(raw_throughput))


class Ju2JmhBenchmarkDataCollector(JmhBenchmarkDataCollector):
  def __init__(self, name):
    super().__init__(name, 'ju2jmh')


class Ju4RunnerBenchmarkDataCollector(JmhBenchmarkDataCollector):
  def __init__(self, name):
    super().__init__(name, 'ju4runner')


def transpose(rows):
  return [list(column) for column in zip(*rows)]


class ExperimentDataCollector:
  def __init__(self, test_batches, output_dir, data_collectors, repetitions):
    self.test_batches = test_batches
    self.output_dir = os.path.abspath(output_dir)
    self.progress_file = os.path.join(self.output_dir, 'progress.json')
    self.progress_backup_file = os.path.join(self.output_dir, 'progress.json.old')
    self.data_collectors = data_collectors
    self.repetitions = repetitions

  def collect_experiment_data(self, output_file, combine_reps):
    finished_batches = self.load_progress()
    field_names = [
      'class',
      'test',
      'config_name',
      'approach',
      'batch'
    ] + (['repetition'] if not combine_reps else []) + [
      'error',
      'measurements',
      'mean',
      'variance',
      'standard_deviation',
      'standard_error',
      'cv',
      'cv_est'
    ]
    self.write_headers(field_names, output_file)
    for batch in range(finished_batches):
      print('Collecting data for batch {:d}/{:d}'.format(batch + 1, finished_batches))
      results = self.collect_batch_results(batch, output_file, combine_reps)
      self.write_results(field_names, results, output_file)
      clear_console_line()

  def collect_batch_results(self, batch, output_file, combine_reps):
    results = [self.aggregate_batch_data(batch, dc, combine_reps) for dc in self.data_collectors]
    if not combine_reps:
      # Sort by test, config_name, repetition.
      results = transpose([transpose(repetition_data) for repetition_data in results])
      results = list(itertools.chain.from_iterable(itertools.chain.from_iterable(results)))
    else:
      # Sort by test, config_name.
      results = transpose(results)
      results = list(itertools.chain.from_iterable(results))
    return results

  def aggregate_batch_data(self, batch, data_collector, combine_reps):
    raw_results = [self.collect_repetition_data(batch, r, data_collector) for r in range(self.repetitions)]
    batch_info = {'config_name': data_collector.name, 'approach': data_collector.approach, 'batch': batch}
    if combine_reps:
      # Transpose the list of results, to get repetitions per test instead of tests per repetition.
      raw_results = transpose(raw_results)
      results = []
      for test, repetition_results in zip(self.test_batches[batch], raw_results):
        base_result = {**batch_info, **test}
        errors = set()
        for repetition_result in repetition_results:
          if 'error' in repetition_result:
            errors.add(repetition_result['error'])
        if errors:
          results.append({**base_result, 'error': ','.join(sorted(errors))})
        else:
          throughput_values = list(itertools.chain.from_iterable(rr['throughput'] for rr in repetition_results))
          results.append({**base_result, **self.compute_throughput_statistics(throughput_values)})
      return results
    else:
      results = []
      for repetition in range(self.repetitions):
        repetition_results = []
        for test, repetition_result in zip(self.test_batches[batch], raw_results[repetition]):
          base_result = {**batch_info, **test, 'repetition': repetition}
          if 'error' in repetition_result:
            repetition_results.append({**base_result, 'error': repetition_result['error']})
          else:
            throughput_values = repetition_result['throughput']
            repetition_results.append({**base_result, **self.compute_throughput_statistics(throughput_values)})
        results.append(repetition_results)
      return results

  def compute_throughput_statistics(self, throughput_values):
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

  def collect_repetition_data(self, batch, repetition, data_collector):
    batch_dir = os.path.join(self.output_dir, 'b{:d}'.format(batch))
    repetition_dir = os.path.join(batch_dir, 'r{:d}'.format(repetition))
    return data_collector.collect_batch_data(self.test_batches[batch], repetition_dir)

  def write_headers(self, fields, output_file):
    with open(output_file, 'w') as f:
      csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
      csv_writer.writeheader()

  def write_results(self, fields, results, output_file):
    with open(output_file, 'a') as f:
      csv_writer = csv.DictWriter(f, fields, dialect=csv.unix_dialect)
      csv_writer.writerows(results)

  def load_progress(self):
    if os.path.exists(self.progress_backup_file):
      progress_file = self.progress_backup_file
    else:
      progress_file = self.progress_file
    with open(progress_file, 'r') as f:
      progress = json.load(f)
    return progress['batch']


def split_into_batches(tests, batch_size):
  return [tests[i:i+batch_size] for i in range(0, len(tests), batch_size)]
 
 
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
  print(config)
  with open(config['test_list'], 'r') as f:
    tests = json.load(f)

  test_batches = split_into_batches(tests, config['batch_size'])

  data_collectors = []
  for runner_config in config['configs']:
    approach = runner_config['approach']
    name = runner_config['name']
    if approach == 'gradle-test':
      data_collector = GradleTestDataCollector(name)
    elif approach == 'ju2jmh':
      data_collector = Ju2JmhBenchmarkDataCollector(name)
    elif approach == 'ju4runner':
      data_collector = Ju4RunnerBenchmarkDataCollector(name)
    data_collectors.append(data_collector)

  output_file = args.output_file if args.output_file else os.path.join(config['output_dir'], 'results.csv')

  data_collector = ExperimentDataCollector(test_batches, config['output_dir'], data_collectors, config['repetitions'])
  data_collector.collect_experiment_data(output_file, args.combine_reps)


if __name__ == '__main__':
  main()
