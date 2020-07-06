import argparse
import pickle
import scipy.stats
import statistics


from batched_experiment.experiment_statistics import ThroughputStatistics


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

  runner1_results = data.get_results(runner=runner1, combine_repetitions=True)
  runner2_results = data.get_results(runner=runner2, combine_repetitions=True)

  deltas = []
  skipped = 0
  for (result1, statistics1), (result2, statistics2) in zip(runner1_results, runner2_results):
    if result1.result.errors or result2.result.errors:
      skipped += 1
    else:
      deltas.append(getattr(statistics1, args.statistic) - getattr(statistics2, args.statistic))
  wilcoxon_result = scipy.stats.wilcoxon(deltas, alternative=args.hypothesis)
  cohen_d = statistics.mean(deltas) / statistics.stdev(deltas)
  print('deltas: {:d}, errors: {:d}, total: {:d}'.format(len(deltas), skipped, len(runner1_results)))
  print('Wilcoxon test: statistic: {}, p-value: {}'.format(wilcoxon_result.statistic, wilcoxon_result.pvalue))
  print("Cohen's d: {}".format(cohen_d))

if __name__ == '__main__':
  main()

