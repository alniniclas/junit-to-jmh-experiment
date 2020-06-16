import argparse
import pickle
import matplotlib.pyplot as plt
import numpy as np


from batched_experiment.experiment_statistics import ThroughputStatistics


def clear_console_line():
  print('\033[F\033[K', end='')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('statistics_file', type=str)
  parser.add_argument('statistic', type=str)
  args = parser.parse_args()

  with open(args.statistics_file, 'rb') as f:
    data = pickle.load(f)

  runner_results = {
    runner: data.get_results(runner=runner, combine_repetitions=True) for runner in data.config.runner_configs
  }

  def has_errors(i):
    for runner in data.config.runner_configs:
      result, statistics = runner_results[runner][i]
      if result.result.errors:
        return True
    return False

  plot_data = {runner: [] for runner in data.config.runner_configs}
  for i in range(len(runner_results[data.config.runner_configs[0]])):
    if has_errors(i):
      continue
    for runner in data.config.runner_configs:
      result, statistics = runner_results[runner][i]
      plot_data[runner].append(getattr(statistics, args.statistic))

  fig, ax = plt.subplots()
  ax.set_ylabel(args.statistic)
  tick_positions = np.arange(1, len(data.config.runner_configs) + 1)
  ax.set_xticks(tick_positions)
  ax.set_xticklabels(runner.name for runner in data.config.runner_configs)
  datapoints = [plot_data[runner] for runner in data.config.runner_configs]
  mins, q1, medians, q3, maxes = np.percentile(datapoints, [0, 25, 50, 75, 100], axis=1)
  ax.scatter(tick_positions, medians, marker='o', color='white', s=30, zorder=3)
  ax.vlines(tick_positions, q1, q3, color='k', lw=5)
  ax.vlines(tick_positions, mins, maxes, color='k', lw=1)
  plot = ax.violinplot(datapoints, showextrema=False)
  for pc in plot['bodies']:
    pc.set_edgecolor('black')
    pc.set_alpha(1)
  plt.show()

if __name__ == '__main__':
  main()

