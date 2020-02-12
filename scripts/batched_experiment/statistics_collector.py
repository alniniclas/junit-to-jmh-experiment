import math
import statistics


from batched_experiment.data_collector import ExperimentDataCollector


class ThroughputStatistics:
  def __init__(self, result):
    self.result = result
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


class StatisticsCollector:
  def __init__(self, config):
    self.data_collector = ExperimentDataCollector(config)

  @property
  def finished_batches(self):
    return self.data_collector.finished_batches

  @property
  def repetitions(self):
    return self.data_collector.repetitions
 
  @staticmethod
  def _compute_statistics(results_dict):
    return {
      key: ThroughputStatistics(results_dict[key]) for key in results_dict
    }

  def collect_repetition_statistics(self, batch, repetition):
    results = self.data_collector.collect_repetition_data(batch, repetition)
    return StatisticsCollector._compute_statistics(results)

  def collect_batch_statistics(self, batch, combine_repetitions=True):
    results = self.data_collector.collect_batch_data(batch, combine_repetitions)
    return StatisticsCollector._compute_statistics(results)
