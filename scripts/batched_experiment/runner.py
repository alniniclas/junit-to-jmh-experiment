import json
import os
import re
import subprocess
import shutil
import xml.etree.ElementTree


from batched_experiment._util import clear_console_line
from batched_experiment.error import BenchmarkExecutionFailedError


class GradleTestRunner:
  def __init__(self, config):
    self.name = config.name
    self.project_root = config.project_root
    self.gradlew = os.path.join(self.project_root, 'gradlew.bat' if os.name == 'nt' else 'gradlew')
    self.subproject_path = config.subproject_path
    subproject_root = os.path.join(self.project_root, *self.subproject_path)
    self.test_results_root = os.path.join(subproject_root, 'build', 'test-results', 'test')
    self.build_test_tmp_dir = os.path.join(subproject_root, 'build', 'tmp', 'test')
    self.executions = config.executions
    self.output_file = config.output_file

  def run_batch(self, tests, output_dir, logging_context=''):
    test_durations = {test: [] for test in tests}
    gradle_command = ':'.join(('', *self.subproject_path, 'test'))
    unit_test_command = [self.gradlew, gradle_command]
    for test in tests:
      qualified_test_name = '{}.{}'.format(test.class_name, test.method_name)
      unit_test_command.extend(['--tests', qualified_test_name])
    for i in range(self.executions):
      print('{} [{} {:d}/{:d}] gradlew {}'.format(logging_context, self.name, i + 1, self.executions, gradle_command))
      subprocess.run(
        unit_test_command, cwd=self.project_root,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
      )
      clear_console_line()
      print('{} [{} {:d}/{:d}] reading output'.format(logging_context, self.name, i + 1, self.executions))
      for test in tests:
        try:
          test_duration = self.get_test_execution_time(test)
          test_durations[test].append(test_duration)
        except BenchmarkExecutionFailedError:
          test_durations[test].append('FAILED')
      clear_console_line()
    if os.path.exists(self.build_test_tmp_dir):
      # Delete build/tmp/test to prevent it from growing indefinitely.
      shutil.rmtree(self.build_test_tmp_dir)
    output = [
      {'class': test.class_name, 'test': test.method_name, 'test_durations': test_durations[test]}
      for test in test_durations
    ]
    output_file = os.path.join(output_dir, self.output_file)
    with open(output_file, 'w') as f:
      json.dump(output, f, indent=4)

  def get_test_execution_time(self, test):
    results_file = os.path.join(self.test_results_root, 'TEST-{}.xml'.format(test.class_name))
    test_cases = xml.etree.ElementTree.parse(results_file).getroot().findall('testcase')
    for test_case in test_cases:
      if test_case.get('name') == test.method_name:
        if test_case.find('failure'):
          raise BenchmarkExecutionFailedError()
        return test_case.get('time')


class JmhBenchmarkRunner:
  def __init__(self, config):
    self.config = config
    self.name = config.name
    self.jar = config.jar
    self.forks = config.forks

  def benchmark_regex(self, test):
    regex = re.escape('{}.{}'.format(test.class_name, test.method_name))
    return '^{}$'.format(regex)

  def run_batch(self, tests, output_dir, logging_context=''):
    for i in range(len(tests)):
      test = tests[i]
      print('{} [{} {:d}/{:d}] {}'.format(
        logging_context, self.config.name, i + 1, len(tests), '{}.{}'.format(test.class_name, test.method_name)
      ))
      self.run_benchmark(test, output_dir)
      clear_console_line()

  def run_benchmark(self, test, output_dir):
    benchmark_output_file = os.path.join(output_dir, self.config.benchmark_output_file(test))
    benchmark_output_dir = os.path.dirname(benchmark_output_file)
    os.makedirs(benchmark_output_dir)
    time_ms = '{:d}ms'.format(self.config.time)
    benchmark_command = [
      'java', '-jar', self.config.jar,
      '-f', str(self.config.forks),
      '-w', time_ms,
      '-r', time_ms,
      '-foe', 'true',
      '-rf', 'json',
      '-rff', benchmark_output_file,
      self.benchmark_regex(test)
    ]
    subprocess.run(benchmark_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class Ju2JmhBenchmarkRunner(JmhBenchmarkRunner):
  def benchmark_regex(self, test):
    regex = re.escape(test.class_name)
    regex += re.escape('._Benchmark')
    regex += r'(?:_\d+)?'
    regex += re.escape('.benchmark_')
    regex += re.escape(test.method_name)
    return '^{}$'.format(regex)


class Ju4RunnerBenchmarkRunner(JmhBenchmarkRunner):
  def benchmark_regex(self, test):
    regex = re.escape('{}_JU4Benchmark.benchmark_{}'.format(test.class_name, test.method_name))
    return '^{}$'.format(regex)


class ExperimentRunner:
  @staticmethod
  def _create_runner(config):
    approaches = {
      'gradle-test': GradleTestRunner,
      'jmh': JmhBenchmarkRunner,
      'ju2jmh': Ju2JmhBenchmarkRunner,
      'ju4runner': Ju4RunnerBenchmarkRunner
    }
    return approaches[config.approach](config)

  def __init__(self, config):
    self.config = config
    self.benchmark_runners = [ExperimentRunner._create_runner(rc) for rc in config.runner_configs]
    self.batch = 0
    self.repetition = 0

  def run_experiment(self):
    self.load_progress()
    while self.batch < len(self.config.test_batches):
      self.run_current_repetition()
      self.save_progress()

  def run_current_repetition(self):
    repetition_dir = self.config.repetition_dir(self.batch, self.repetition)
    if os.path.exists(repetition_dir):
      shutil.rmtree(repetition_dir)
    os.makedirs(repetition_dir)
    for i in range(len(self.benchmark_runners)):
      logging_context = '[Batch {:d}/{:d}, repetition {:d}/{:d}, runner {:d}/{:d}]'.format(
        self.batch + 1, len(self.config.test_batches),
        self.repetition + 1, self.config.repetitions,
        i + 1, len(self.benchmark_runners)
      )
      runner = self.benchmark_runners[i]
      runner.run_batch(self.config.test_batches[self.batch], repetition_dir, logging_context=logging_context)
    self.repetition += 1
    if self.repetition >= self.config.repetitions:
      self.batch += 1
      self.repetition = 0

  def load_progress(self):
    if os.path.exists(self.config.progress_backup_file):
      if os.path.exists(self.config.progress_file):
        os.remove(self.config.progress_file)
      os.rename(self.config.progress_backup_file, self.progress_file)
    if os.path.exists(self.config.progress_file):
      with open(self.config.progress_file, 'r') as f:
        progress = json.load(f)
      self.batch = progress['batch']
      self.repetition = progress['repetition']

  def save_progress(self):
    progress = {'batch': self.batch, 'repetition': self.repetition}
    if os.path.exists(self.config.progress_file):
      os.rename(self.config.progress_file, self.config.progress_backup_file)
    with open(self.config.progress_file, 'w') as f:
      json.dump(progress, f)
      f.flush()
      os.fsync(f.fileno())
    if os.path.exists(self.config.progress_backup_file):
      os.remove(self.config.progress_backup_file)
