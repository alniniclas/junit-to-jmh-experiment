import argparse
import pickle
import scipy.stats


from batched_experiment.experiment_statistics import ThroughputStatistics
from summary_statistics import summary_statistics


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('statistics_file', type=str)
  parser.add_argument('runner1', type=str)
  parser.add_argument('runner2', type=str)
  parser.add_argument('statistic', type=str)
  parser.add_argument('--hypothesis', type=str, default='two-sided')
  args = parser.parse_args()

  with open(args.statistics_file, 'rb') as f:
    data = pickle.load(f)

  def find_runner(name):
    for runner in data.config.runner_configs:
      if runner.name == name:
        return runner
    raise ValueError('invalid runner name {}, valid runners are {}'.format(
      name, ', '.join([r.name for r in data.config.runner_configs])
    ))
      
  runner1 = find_runner(args.runner1)
  runner2 = find_runner(args.runner2)

  results = zip(
    data.get_results(runner=runner1, combine_repetitions=True),
    data.get_results(runner=runner2, combine_repetitions=True)
  )

  runner1_statistic_vals = []
  runner2_statistic_vals = []
  skipped = 0
  for (result1, statistics1), (result2, statistics2) in results:
    if result1.result.errors or result2.result.errors:
      skipped += 1
    else:
      runner1_statistic_vals.append(getattr(statistics1, args.statistic))
      runner2_statistic_vals.append(getattr(statistics2, args.statistic))
  deltas = [val1 - val2 for val1, val2 in zip(runner1_statistic_vals, runner2_statistic_vals)]

  runner1_summary = summary_statistics(runner1_statistic_vals)
  runner2_summary = summary_statistics(runner2_statistic_vals)
  deltas_summary = summary_statistics(deltas)
  wilcoxon_result = scipy.stats.wilcoxon(deltas, alternative=args.hypothesis)
  cohen_d = deltas_summary.mean / deltas_summary.stddev

  print('deltas: {:d}, errors: {:d}, total: {:d}'.format(len(deltas), skipped, len(deltas) + skipped))
  print('{} {}: {}'.format(runner1.name, args.statistic, runner1_summary))
  print('{} {}: {}'.format(runner2.name, args.statistic, runner2_summary))
  print('{} delta: {}'.format(args.statistic, deltas_summary))
  print('Wilcoxon test: statistic: {}, p-value: {}'.format(wilcoxon_result.statistic, wilcoxon_result.pvalue))
  print("Cohen's d: {}".format(cohen_d))

if __name__ == '__main__':
  main()

