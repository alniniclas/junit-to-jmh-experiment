import argparse
import batched_experiment.runner
import batched_experiment.config


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  args = parser.parse_args()

  config = batched_experiment.config.BatchedExperimentConfiguration.parse_from_file(args.config)

  experiment_runner = batched_experiment.runner.ExperimentRunner(config)
  experiment_runner.run_experiment()


if __name__ == '__main__':
  main()
