import argparse
import json
import csv
import pickle


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('statistics_file', type=str)
  parser.add_argument('output_file', type=str)
  args = parser.parse_args()

  with open(args.statistics_file, 'rb') as f:
    statistics = pickle.load(f)

  columns = [
    'class',
    'test',
    'runner_name',
    'approach',
    'batch',
    'error_count',
    'errors'
  ]
  rows = []
  for result, _ in statistics.get_results(combine_repetitions=True):
    if not result.result.errors:
      continue
    repetitions = statistics.get_results(batch=result.batch, test=result.test, runner=result.runner)
    row = {
      'class': result.test.class_name,
      'test': result.test.method_name,
      'runner_name': result.runner.name,
      'approach': result.runner.approach,
      'batch': result.batch,
      'error_count': sum(1 for r, _ in repetitions if r.result.errors),
      'errors': ';'.join(','.join(r.result.errors) for r, _ in repetitions)
    }
    rows.append(row)

  with open(args.output_file, 'w') as f:
    csv_writer = csv.DictWriter(f, columns, dialect=csv.unix_dialect)
    csv_writer.writeheader()
    csv_writer.writerows(rows)


if __name__ == '__main__':
  main()
