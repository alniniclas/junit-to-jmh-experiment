import argparse
import json
import pickle


from batched_experiment.config import Test
from batched_experiment.slowdown_comparison import TwoTestComparison, SelfComparison, perform_comparisons


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('statistics_file', type=str)
  parser.add_argument('test_comparisons', type=str)
  parser.add_argument('alpha', type=float)
  parser.add_argument('output_file', type=str)
  args = parser.parse_args()

  with open(args.statistics_file, 'rb') as f:
    statistics = pickle.load(f)

  def parse_test(d):
    return Test(d['class'], d['test'])

  def parse_comparison(d):
    if 'baseline' in d:
      relative_throughput = d['baseline_work'] / d['comparison_work']
      return TwoTestComparison(parse_test(d['baseline']), parse_test(d['comparison']), relative_throughput)
    else:
      return SelfComparison(parse_test(d['test']))

  with open(args.test_comparisons, 'r') as f:
    test_comparisons = [parse_comparison(d) for d in json.load(f)]

  results = perform_comparisons(statistics, test_comparisons, args.alpha)
  
  with open(args.output_file, 'wb') as f:
    pickle.dump(results, f)


if __name__ == '__main__':
  main()
