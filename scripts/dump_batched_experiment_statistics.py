import argparse
import pickle
import time


from batched_experiment.experiment_statistics import ExperimentStatistics


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('data_file', type=str)
  parser.add_argument('output_file', type=str)
  args = parser.parse_args()

  with open(args.data_file, 'rb') as f:
    data = pickle.load(f)

  latest_update = None
  def progress_callback(current_separate=None, total_separate=None, current_combined=None, total_combined=None):
    nonlocal latest_update
    current_time = time.monotonic()
    if latest_update is None or current_time - latest_update >= 1:
      latest_update = current_time
      progress = []
      if current_separate is not None:
        progress.append('separate {:d}/{:d}'.format(current_separate + 1, total_separate))
      if current_combined is not None:
        progress.append('combined {:d}/{:d}'.format(current_combined + 1, total_combined))
      print('processing {}'.format(', '.join(progress)))

  statistics = ExperimentStatistics.from_experiment_results(data, progress_callback=progress_callback)

  with open(args.output_file, 'wb') as f:
    pickle.dump(statistics, f)


if __name__ == '__main__':
  main()
