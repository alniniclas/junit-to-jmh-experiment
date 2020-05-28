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

  batches = []
  
  for batch in range(data_collector.finished_batches):
    print('reading batch {:d}/{:d}'.format(batch + 1, data_collector.finished_batches))
    batches.append(data_collector.collect_batch_data(batch, combine_repetitions=False))
    clear_console_line()

  output = {
    'config': config,
    'batches': batches
  }

  with open(args.output_file, 'wb') as f:
    pickle.dump(output, f)


if __name__ == '__main__':
  main()
