import argparse
import json
import csv
import pickle


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('comparisons_file', type=str)
  parser.add_argument('output_file', type=str)
  args = parser.parse_args()

  with open(args.comparisons_file, 'rb') as f:
    comparison_results = pickle.load(f)

  columns = [
    'baseline_class',
    'baseline_test',
    'comparison_class',
    'comparison_test',
    'config_name',
    'approach',
    'baseline_batch',
    'comparison_batch',
    'baseline_errors',
    'comparison_errors',
    'baseline_measurements',
    'comparison_measurements',
    'baseline_mean',
    'comparison_mean',
    'throughput_ratio',
    'expected_throughput_ratio',
    'baseline_standard_deviation',
    'comparison_standard_deviation',
    'alpha',
    'comparisons',
    'significant',
    'p_value'
  ]
  rows = []
  for result in comparison_results:
    baseline_result = result.baseline_results_combined
    baseline_statistics = result.baseline_statistics_combined
    comparison_result = result.comparison_results_combined
    comparison_statistics = result.comparison_statistics_combined
    row = {
      'baseline_class': baseline_result.test.class_name,
      'baseline_test': baseline_result.test.method_name,
      'comparison_class': comparison_result.test.class_name,
      'comparison_test': comparison_result.test.method_name,
      'config_name': baseline_result.runner.name,
      'approach': baseline_result.runner.approach,
      'baseline_batch': baseline_result.batch,
      'comparison_batch': comparison_result.batch,
      'baseline_errors': ','.join(sorted(set(baseline_result.result.errors))),
      'comparison_errors': ','.join(sorted(set(comparison_result.result.errors))),
      'baseline_measurements': baseline_statistics.measurements,
      'comparison_measurements': comparison_statistics.measurements,
      'baseline_mean': baseline_statistics.mean,
      'comparison_mean': comparison_statistics.mean,
      'throughput_ratio': (
        comparison_statistics.mean / baseline_statistics.mean
        if baseline_statistics.mean and comparison_statistics.mean else None
      ),
      'expected_throughput_ratio': result.comparison.expected_relative_throughput,
      'baseline_standard_deviation': baseline_statistics.stddev,
      'comparison_standard_deviation': comparison_statistics.stddev,
      'alpha': result.alpha,
      'comparisons': result.total_tests,
      'significant': result.significant_tests,
      'p_value': result.binomial_test_result
    }
    rows.append(row)

  with open(args.output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, columns, dialect=csv.unix_dialect)
    csv_writer.writeheader()
    csv_writer.writerows(rows)


if __name__ == '__main__':
  main()
