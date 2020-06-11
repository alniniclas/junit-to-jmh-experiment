import argparse
import pickle
import scipy.stats


from batched_experiment.experiment_statistics import ThroughputStatistics


def clear_console_line():
  print('\033[F\033[K', end='')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('data_file', type=str)
  parser.add_argument('runner1', type=str)
  parser.add_argument('runner2', type=str)
  parser.add_argument('statistic', type=str)
  parser.add_argument('--hypothesis', type=str, default='two-sided')
  args = parser.parse_args()

  with open(args.data_file, 'rb') as f:
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

  def statistic_from_result(result):
    return getattr(ThroughputStatistics(result.result), args.statistic)
  deltas = []
  skipped = 0
  i = 0
  for runner1_result, runner2_result in zip(runner1_results, runner2_results):
    i += 1
    print('{:d}/{:d}, {:d} skipped'.format(i, len(runner1_results), skipped))
    if runner1_result.result.errors or runner2_result.result.errors:
      skipped += 1
    else:
      deltas.append(statistic_from_result(runner1_result) - statistic_from_result(runner2_result))
    clear_console_line()
  print('deltas: {:d}, errors: {:d}, total: {:d}'.format(len(deltas), skipped, i))
  print(scipy.stats.wilcoxon(deltas, alternative=args.hypothesis))

if __name__ == '__main__':
  main()

