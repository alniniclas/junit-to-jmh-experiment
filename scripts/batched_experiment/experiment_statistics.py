import math
import statistics


class ThroughputStatistics:
  def __init__(self, result):
    if not result.errors:
      throughput_values = result.throughput
      self.measurements = len(throughput_values)
      self.mean = statistics.mean(throughput_values)
      self.variance = statistics.variance(throughput_values)
      self.stddev = statistics.stdev(throughput_values)
      self.stderr = self.stddev / math.sqrt(self.measurements)
      self.cv = self.stddev / self.mean
      # Unbiased estimator for normally distributed data.
      self.cv_est = (1 + (1 / (4 * self.measurements))) * self.cv
    else:
      self.measurements = None
      self.mean = None
      self.variance = None
      self.stddev = None
      self.stderr = None
      self.cv = None
      self.cv_est = None

class ExperimentStatistics:
  def __init__(self, results, separate, combined):
    self._results = results
    self._separate = separate
    self._combined = combined

  @staticmethod
  def from_experiment_results(experiment_results, progress_callback=None):
    separate_results = experiment_results.get_results(combine_repetitions=False)
    separate_statistics = {}
    combined_statistics = {}
    for i in range(len(separate_results)):
      if progress_callback:
        progress_callback(current_separate=i, total_separate=len(separate_results))
      result = separate_results[i]
      key = (result.batch, result.repetition, result.test, result.runner)
      separate_statistics[key] = ThroughputStatistics(result.result)
    combined_results = experiment_results.get_results(combine_repetitions=True)
    for i in range(len(combined_results)):
      if progress_callback:
        progress_callback(current_combined=i, total_combined=len(combined_results))
      result = combined_results[i]
      key = (result.batch, result.test, result.runner)
      combined_statistics[key] = ThroughputStatistics(result.result)
    return ExperimentStatistics(experiment_results, separate_statistics, combined_statistics)

  @property
  def config(self):
    return self._results.config

  def get_results(self, batch=None, repetition=None, test=None, runner=None, combine_repetitions=False):
    results = self._results.get_results(
      batch=batch, repetition=repetition, test=test, runner=runner,
      combine_repetitions=combine_repetitions
    )
    def get_statistics(result):
      if not combine_repetitions:
        return self._separate[result.batch, result.repetition, result.test, result.runner]
      else:
        return self._combined[result.batch, result.test, result.runner]
    return [(result, get_statistics(result)) for result in results]
