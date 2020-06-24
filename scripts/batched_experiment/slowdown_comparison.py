import scipy.stats


from batched_experiment.config import Test
from batched_experiment.experiment_data import Result, ExperimentResult
from batched_experiment.experiment_statistics import ThroughputStatistics
from functools import cached_property


class TwoTestComparison:
  def __init__(self, baseline, comparison, expected_relative_throughput):
    self.baseline = baseline
    self.comparison = comparison
    self.expected_relative_throughput = expected_relative_throughput

  def get_result_pairs(self, experiment_statistics, runner):
    baseline_results = experiment_statistics.get_results(test=self.baseline, runner=runner)
    comparison_results = experiment_statistics.get_results(test=self.comparison, runner=runner)
    return zip(baseline_results, comparison_results)


class SelfComparison:
  def __init__(self, test):
    self.baseline = test
    self.comparison = test
    self.expected_relative_throughput = 1

  def get_result_pairs(self, experiment_statistics, runner):
    results = experiment_statistics.get_results(test=self.baseline, runner=runner)
    return zip(results[::2], results[1::2])


class RunComparisonResult:
  def __init__(self, comparison, runner, baseline_result, comparison_result):
    self.comparison = comparison
    self.runner = runner
    self.baseline_result, self.baseline_statistics = baseline_result
    self.comparison_result, self.comparison_statistics = comparison_result

  @cached_property
  def mwu_result(self):
    if self.baseline_result.result.errors or self.comparison_result.result.errors:
      return None
    return scipy.stats.mannwhitneyu(
      self.baseline_result.result.throughput, self.comparison_result.result.throughput,
      use_continuity=False, alternative='greater'
    )

  @cached_property
  def relative_throughput(self):
    if self.baseline_result.errors or self.comparison_result.errors:
      return None
    return self.comparison_statistics.mean / self.baseline_statistics[1].mean


class TestComparisonResult:
  def __init__(self, comparison, runner, alpha, run_comparison_results):
    self.comparison = comparison
    self.runner = runner
    self.alpha = alpha
    self.run_comparison_results = run_comparison_results

  @cached_property
  def _test_results(self):
    significant = 0
    total = 0
    for run_comparison_result in self.run_comparison_results:
      mwu_result = run_comparison_result.mwu_result
      if not mwu_result:
        continue
      if mwu_result[1] < self.alpha:
        significant += 1
      total += 1
    return significant, total

  @property
  def significant_tests(self):
    significant, _ = self._test_results
    return significant

  @property
  def total_tests(self):
    _, total = self._test_results
    return total

  @cached_property
  def binomial_test_result(self):
    if self.total_tests < 1:
      return None
    return scipy.stats.binom_test(self.significant_tests, n=self.total_tests, p=self.alpha, alternative='greater')

  @cached_property
  def baseline_results_combined(self):
    batch = self.run_comparison_results[0].baseline_result.batch
    result = Result.merge(
      run_comparison_result.baseline_result.result for run_comparison_result in self.run_comparison_results
    )
    return ExperimentResult(batch, None, self.comparison.baseline, self.runner, result)

  @cached_property
  def baseline_statistics_combined(self):
    return ThroughputStatistics(self.baseline_results_combined.result)

  @cached_property
  def comparison_results_combined(self):
    batch = self.run_comparison_results[0].comparison_result.batch
    result = Result.merge(
      run_comparison_result.comparison_result.result for run_comparison_result in self.run_comparison_results
    )
    return ExperimentResult(batch, None, self.comparison.comparison, self.runner, result)

  @cached_property
  def comparison_statistics_combined(self):
    return ThroughputStatistics(self.comparison_results_combined.result)


def perform_comparisons(statistics, comparisons, alpha):
  results = []
  for test_comparison in comparisons:
    for runner in statistics.config.runner_configs:
      pairs = test_comparison.get_result_pairs(statistics, runner)
      run_comparison_results = []
      for baseline, comparison in pairs:
        run_comparison_results.append(RunComparisonResult(test_comparison, runner, baseline, comparison))
      results.append(TestComparisonResult(test_comparison, runner, alpha, run_comparison_results))
  return results
