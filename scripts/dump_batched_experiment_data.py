import argparse
import batched_experiment.data_collector
import pickle


def clear_console_line():
  print('\033[F\033[K', end='')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  parser.add_argument('output_file', type=str)
  args = parser.parse_args()

  config = batched_experiment.config.BatchedExperimentConfiguration.parse_from_file(args.config)

  data_collector = batched_experiment.data_collector.ExperimentDataCollector(config)

  # Temporary message to simplify the callback code.
  print('reading batch 0/0, repetition 0/0')
  def progress_callback(current_batch=0, current_repetition=0, total_batches=0, total_repetitions=0):
    clear_console_line()
    print('reading batch {:d}/{:d}, repetition {:d}/{:d}'.format(
      current_batch + 1, total_batches, current_repetition + 1, total_repetitions
    ))

  experiment_results = data_collector.collect_experiment_data(progress_callback)
  clear_console_line()

  with open(args.output_file, 'wb') as f:
    pickle.dump(experiment_results, f)


if __name__ == '__main__':
  main()
