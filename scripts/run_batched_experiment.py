import abc
import argparse
import json
import os
import time
import re
import subprocess
import xml.etree.ElementTree
import shutil


class BenchmarkExecutionFailedError(Exception):
  pass


def clear_console_line():
  print('\033[F\033[K', end='')


class GradleTestRunner:
  def __init__(self, name, project_root, executions):
    self.name = name
    self.project_root = os.path.abspath(project_root)
    self.gradlew = os.path.join(self.project_root, 'gradlew.bat' if os.name == 'nt' else 'gradlew')
    self.test_results_root = os.path.join(self.project_root, 'build', 'test-results', 'test')
    self.build_test_tmp_dir = os.path.join(self.project_root, 'build', 'tmp', 'test')
    self.executions = executions

  def run_batch(self, tests, output_dir, logging_context=''):
    test_durations = {(test['class'], test['test']): [] for test in tests}
    test_names = ['{}.{}'.format(test['class'], test['test']) for test in tests]
    unit_test_command = [self.gradlew, 'test']
    for test in tests:
      qualified_test_name = '{}.{}'.format(test['class'], test['test'])
      unit_test_command.extend(['--tests', qualified_test_name])
    for i in range(self.executions):
      print('{} [{} {:d}/{:d}] gradlew test'.format(logging_context, self.name, i + 1, self.executions))
      subprocess.run(
        unit_test_command, cwd=self.project_root,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
      )
      clear_console_line()
      print('{} [{} {:d}/{:d}] reading output'.format(logging_context, self.name, i + 1, self.executions))
      for test in tests:
        try:
          test_duration = self.get_test_execution_time(test['class'], test['test'])
          test_durations[test['class'], test['test']].append(test_duration)
        except BenchmarkExecutionFailedError:
          test_durations[test['class'], test['test']].append('FAILED')
      clear_console_line()
    if os.path.exists(self.build_test_tmp_dir):
      # Delete build/tmp/test to prevent it from growing indefinitely.
      shutil.rmtree(self.build_test_tmp_dir)
    output = [
      {'class': class_name, 'test': test_name, 'test_durations': test_durations[class_name, test_name]}
      for class_name, test_name in test_durations
    ]
    output_file = os.path.join(output_dir, '{}_output.json'.format(self.name))
    with open(output_file, 'w') as f:
      json.dump(output, f, indent=4)

  def get_test_execution_time(self, test_class, test_name):
    results_file = os.path.join(self.test_results_root, 'TEST-{}.xml'.format(test_class))
    test_cases = xml.etree.ElementTree.parse(results_file).getroot().findall('testcase')
    for test_case in test_cases:
      if test_case.get('name') == test_name:
        if test_case.find('failure'):
          raise BenchmarkExecutionFailedError()
        return test_case.get('time')


class JmhBenchmarkRunner:
  def __init__(self, name, jar, forks, time):
    self.name = name
    self.jar = os.path.abspath(jar)
    self.forks = forks
    self.time_ms = '{:d}ms'.format(time)

  def benchmark_regex(self, class_name, test_name):
    raise NotImplementedError()

  def run_batch(self, tests, output_dir, logging_context=''):
    runner_output_dir = os.path.join(output_dir, self.name)
    os.makedirs(runner_output_dir)
    for i in range(len(tests)):
      test = tests[i]
      print('{} [{} {:d}/{:d}] {}'.format(
        logging_context, self.name, i + 1, len(tests), '{}.{}'.format(test['class'], test['test'])
      ))
      self.run_benchmark(test['class'], test['test'], runner_output_dir)
      clear_console_line()

  def run_benchmark(self, class_name, test_name, runner_output_dir):
    benchmark_output_dir = os.path.join(runner_output_dir, class_name, test_name)
    benchmark_output_file = os.path.join(benchmark_output_dir, 'output.json')
    os.makedirs(benchmark_output_dir)
    benchmark_command = [
      'java', '-jar', self.jar,
      '-f', str(self.forks),
      '-w', self.time_ms,
      '-r', self.time_ms,
      '-foe', 'true',
      '-rf', 'json',
      '-rff', benchmark_output_file,
      self.benchmark_regex(class_name, test_name)
    ]
    subprocess.run(benchmark_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class Ju2JmhBenchmarkRunner(JmhBenchmarkRunner):
  def benchmark_regex(self, class_name, test_name):
    regex = re.escape(class_name)
    regex += re.escape('._Benchmark')
    regex += r'(?:_\d+)?'
    regex += re.escape('.benchmark_')
    regex += re.escape(test_name)
    return '^{}$'.format(regex)


class Ju4RunnerBenchmarkRunner(JmhBenchmarkRunner):
  def benchmark_regex(self, class_name, test_name):
    regex = re.escape('{}_JU4Benchmark.benchmark_{}'.format(class_name, test_name))
    return '^{}$'.format(regex)


class ExperimentRunner:
  def __init__(self, test_batches, output_dir, benchmark_runners, repetitions):
    self.test_batches = test_batches
    self.output_dir = os.path.abspath(output_dir)
    self.progress_file = os.path.join(self.output_dir, 'progress.json')
    self.progress_backup_file = os.path.join(self.output_dir, 'progress.json.old')
    self.benchmark_runners = benchmark_runners
    self.repetitions = repetitions
    self.batch = 0
    self.repetition = 0

  def run_experiment(self):
    self.load_progress()
    while self.batch < len(self.test_batches):
      self.run_current_repetition()
      self.save_progress()

  def run_current_repetition(self):
    batch_dir = os.path.join(self.output_dir, 'b{:d}'.format(self.batch))
    repetition_dir = os.path.join(batch_dir, 'r{:d}'.format(self.repetition))
    if os.path.exists(repetition_dir):
      shutil.rmtree(repetition_dir)
    os.makedirs(repetition_dir)
    for i in range(len(self.benchmark_runners)):
      logging_context = '[Batch {:d}/{:d}, repetition {:d}/{:d}, runner {:d}/{:d}]'.format(
        self.batch + 1, len(self.test_batches),
        self.repetition + 1, self.repetitions,
        i + 1, len(self.benchmark_runners)
      )
      runner = self.benchmark_runners[i]
      runner.run_batch(self.test_batches[self.batch], repetition_dir, logging_context=logging_context)
    self.repetition += 1
    if self.repetition >= self.repetitions:
      self.batch += 1
      self.repetition = 0

  def load_progress(self):
    if os.path.exists(self.progress_backup_file):
      if os.path.exists(self.progress_file):
        os.remove(self.progress_file)
      os.rename(self.progress_backup_file, self.progress_file)
    if os.path.exists(self.progress_file):
      with open(self.progress_file, 'r') as f:
        progress = json.load(f)
      self.batch = progress['batch']
      self.repetition = progress['repetition']

  def save_progress(self):
    progress = {'batch': self.batch, 'repetition': self.repetition}
    if os.path.exists(self.progress_file):
      os.rename(self.progress_file, self.progress_backup_file)
    with open(self.progress_file, 'w') as f:
      json.dump(progress, f)
      f.flush()
      os.fsync(f.fileno())
    if os.path.exists(self.progress_backup_file):
      os.remove(self.progress_backup_file)


def split_into_batches(tests, batch_size):
  return [tests[i:i+batch_size] for i in range(0, len(tests), batch_size)]


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  args = parser.parse_args()
  
  with open(args.config, 'r') as f:
    config = json.load(f)
  print(config)
  with open(config['test_list'], 'r') as f:
    tests = json.load(f)

  test_batches = split_into_batches(tests, config['batch_size'])

  benchmark_runners = []
  for runner_config in config['configs']:
    approach = runner_config['approach']
    name = runner_config['name']
    if approach == 'gradle-test':
      benchmark_runner = GradleTestRunner(name, runner_config['project_root'], runner_config['executions'])
    elif approach == 'ju2jmh':
      benchmark_runner = Ju2JmhBenchmarkRunner(name, runner_config['jar'], runner_config['forks'], runner_config['time'])
    elif approach == 'ju4runner':
      benchmark_runner = Ju4RunnerBenchmarkRunner(name, runner_config['jar'], runner_config['forks'], runner_config['time'])
    benchmark_runners.append(benchmark_runner)

  experiment_runner = ExperimentRunner(test_batches, config['output_dir'], benchmark_runners, config['repetitions'])
  experiment_runner.run_experiment()


if __name__ == '__main__':
  main()
