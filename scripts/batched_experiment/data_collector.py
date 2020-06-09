import itertools
import json
import os


from batched_experiment._util import clear_console_line
from batched_experiment.config import Test
from batched_experiment.error import BenchmarkExecutionFailedError
from batched_experiment.experiment_data import ExperimentResult, ExperimentResults, Result


class RunnerDataCollector:
  def __init__(self, config):
    self.config = config


class GradleTestDataCollector(RunnerDataCollector):
  def collect_repetition_data(self, tests, repetition_output_dir):
    repetition_output_file = os.path.join(repetition_output_dir, self.config.output_file)
    with open(repetition_output_file, 'r') as f:
      repetition_output = json.load(f)
    test_durations = {Test(t['class'], t['test']): t['test_durations'] for t in repetition_output}
    results = {}
    for test in tests:
      try:
        result = Result(throughput=self.durations_to_throughput(test_durations[test]))
      except BenchmarkExecutionFailedError:
        result = Result(errors=['FAILED'])
      except ZeroDivisionError:
        result = Result(errors=['ZERO_DURATION'])
      results[test] = result
    return results

  def durations_to_throughput(self, durations):
    for duration in durations:
      if duration == 'FAILED':
        raise BenchmarkExecutionFailedError()
    return [1.0 / float(d) for d in durations]


class JmhBenchmarkDataCollector(RunnerDataCollector):
  def collect_repetition_data(self, tests, repetition_output_dir):
    results = {}
    for test in tests:
      try:
        result = Result(throughput=self.collect_benchmark_data(test, repetition_output_dir))
      except BenchmarkExecutionFailedError:
        result = Result(errors=['FAILED'])
      results[test] = result
    return results

  def collect_benchmark_data(self, test, repetition_output_dir):
    benchmark_output_file = os.path.join(repetition_output_dir, self.config.benchmark_output_file(test))
    if os.path.getsize(benchmark_output_file) == 0:
      # An empty results file means that the benchmark execution failed.
      raise BenchmarkExecutionFailedError()
    with open(benchmark_output_file, 'r') as f:
      raw_throughput = json.load(f)[0]['primaryMetric']['rawData']
    return list(itertools.chain.from_iterable(raw_throughput))


class ExperimentDataCollector:
  @staticmethod
  def _create_collector(config):
    approaches = {
      'gradle-test': GradleTestDataCollector,
      'jmh': JmhBenchmarkDataCollector,
      'ju2jmh': JmhBenchmarkDataCollector,
      'ju4runner': JmhBenchmarkDataCollector
    }
    return approaches[config.approach](config)
    
  def __init__(self, config):
    self.config = config
    self._progress = None
    self.runner_data_collectors = [ExperimentDataCollector._create_collector(rc) for rc in config.runner_configs]

  def _load_progress(self):
    if os.path.exists(self.config.progress_backup_file):
      progress_file = self.config.progress_backup_file
    else:
      progress_file = self.config.progress_file
    with open(progress_file, 'r') as f:
      progress = json.load(f)
    self._progress = progress['batch']

  @property
  def finished_batches(self):
    if self._progress is None:
      self._load_progress()
    return self._progress

  @property
  def repetitions(self):
    return self.config.repetitions

  def _collect_repetition_data(self, batch, repetition):
    tests = self.config.test_batches[batch]
    repetition_dir = self.config.repetition_dir(batch, repetition)
    collector_results = {
      collector.config: collector.collect_repetition_data(tests, repetition_dir)
      for collector in self.runner_data_collectors
    }
    results = []
    for config in collector_results:
      for test in collector_results[config]:
        results.append(ExperimentResult(batch, repetition, test, config, collector_results[config][test]))
    return results

  def collect_experiment_data(self, progress_callback=None):
    results = []
    for batch in range(self.finished_batches):
      for repetition in range(self.repetitions):
        if progress_callback:
          progress_callback(
            current_batch=batch, current_repetition=repetition, total_batches=self.finished_batches,
            total_repetitions=self.repetitions
          )
        results.extend(self._collect_repetition_data(batch, repetition))
    return ExperimentResults.from_results(self.config, results)
