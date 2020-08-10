import argparse
import json


from summary_statistics import summary_statistics


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input_file', type=str)
  parser.add_argument('--no-outliers', dest='plot_outliers', default=True, action='store_false')
  parser.add_argument('--jitter', default=0.0, type=float)
  args = parser.parse_args()

  with open(args.input_file, 'r') as f:
    data = json.load(f)

  for series in data['series']:
    statistics = summary_statistics(series['values'])
    label = '{} {}'.format(series['name'], data['ylabel']) if 'ylabel' in data else series['name']
    print('{}: {}'.format(label, statistics))


if __name__ == '__main__':
  main()
