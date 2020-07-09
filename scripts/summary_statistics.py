import statistics
import math

from collections import namedtuple


SummaryStatistics = namedtuple('SummaryStatistics', ('measurements', 'mean', 'variance', 'stddev', 'stderr', 'cv'))


def summary_statistics(values):
  measurements = len(values)
  mean = statistics.mean(values)
  variance = statistics.variance(values)
  stddev = statistics.stdev(values)
  stderr = stddev / math.sqrt(measurements)
  cv = stddev / mean
  return SummaryStatistics(measurements, mean, variance, stddev, stderr, cv)
