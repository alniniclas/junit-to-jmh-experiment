import math
import statistics


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
