import statistics
import math

from collections import namedtuple


SummaryStatistics = namedtuple(
  'SummaryStatistics',
  ('measurements', 'mean', 'median', 'min', 'max', 'quartiles', 'variance', 'stddev', 'stderr', 'cv')
)


def summary_statistics(values):
  measurements = len(values)
  mean = statistics.mean(values)
  median = statistics.median(values)
  min_val = min(values)
  max_val = max(values)
  quantiles = statistics.quantiles(values)
  variance = statistics.variance(values)
  stddev = statistics.stdev(values)
  stderr = stddev / math.sqrt(measurements)
  cv = stddev / mean
  return SummaryStatistics(
    measurements, mean, median, min_val, max_val, quantiles, variance, stddev, stderr, cv
  )
