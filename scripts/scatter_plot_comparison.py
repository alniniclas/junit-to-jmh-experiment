import argparse
import math
import pickle


import matplotlib.pyplot as plt

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('statistics_file', type=str)
  parser.add_argument('runner1', type=str)
  parser.add_argument('runner2', type=str)
  parser.add_argument('statistic', type=str)
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

  runner1_statistic = []
  runner2_statistic = []
  for (result1, statistics1), (result2, statistics2) in zip(runner1_results, runner2_results):
    if not result1.result.errors and not result2.result.errors:
      runner1_statistic.append(getattr(statistics1, args.statistic))
      runner2_statistic.append(getattr(statistics2, args.statistic))

  max_val = max(max(runner1_statistic), max(runner2_statistic))
  fig, ax = plt.subplots()
  ax.set_xlabel('{} {}'.format(runner1.name, args.statistic))
  ax.set_ylabel('{} {}'.format(runner2.name, args.statistic))
  ax.scatter(runner1_statistic, runner2_statistic, s=5, alpha=0.3, edgecolors='none')
  plt.show()


if __name__ == '__main__':
  main()

