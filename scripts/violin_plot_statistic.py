import argparse
import pickle


from violin_plot import DataSeries, violin_plot


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('statistics_file', type=str)
  parser.add_argument('statistic', type=str)
  parser.add_argument('--no-outliers', dest='plot_outliers', default=True, action='store_false')
  parser.add_argument('--jitter', default=0.0, type=float)
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

  violin_plot(
    [DataSeries(runner.name, plot_data[runner]) for runner in data.config.runner_configs],
    ylabel=args.statistic,
    plot_outliers=args.plot_outliers,
    outlier_jitter=args.jitter
  )


if __name__ == '__main__':
  main()

