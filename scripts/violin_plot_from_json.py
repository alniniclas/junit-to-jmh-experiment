import argparse
import json


from violin_plot import DataSeries, violin_plot


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input_file', type=str)
  parser.add_argument('--no-outliers', dest='plot_outliers', default=True, action='store_false')
  parser.add_argument('--jitter', default=0.0, type=float)
  args = parser.parse_args()

  with open(args.input_file, 'r') as f:
    data = json.load(f)

  violin_plot(
    [DataSeries(series['name'], series['values']) for series in data['series']],
    xlabel=data.get('xlabel'),
    ylabel=data.get('ylabel'),
    plot_outliers=args.plot_outliers,
    outlier_jitter=args.jitter
  )


if __name__ == '__main__':
  main()

