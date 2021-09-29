import argparse
import csv
import numpy as np

from bar_chart import bar_chart

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input_file', type=str)
  parser.add_argument('--title', type=str)
  parser.add_argument('--xlabel', type=str)
  parser.add_argument('--ylabel', type=str)
  parser.add_argument('--expected', type=str)
  parser.add_argument('--size', type=str)
  parser.add_argument('--legend', type=str)
  parser.add_argument('--xlim', type=str)
  parser.add_argument('--ylim', type=str)
  args = parser.parse_args()

  with open(args.input_file, 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

  column_labels = rows[0][1:]
  row_labels = [row[0] for row in rows[1:]]
  data = np.array([[float(value) for value in row[1:]] for row in rows[1:]]).T

  expected = None
  if args.expected:
    expected = [x.split('/') for x in args.expected.split(',')]
    expected = [float(x[0]) if len(x) == 1 else float(x[0])/float(x[1]) for x in expected]

  size = None
  if args.size:
    size = np.array([float(d) for d in args.size.split(',')])

  legend = None
  if args.legend:
    legend_args = args.legend.split(',')
    legend = {
      'bbox_to_anchor': (float(legend_args[0]), float(legend_args[1])),
      'loc': legend_args[2].strip(),
      'ncol': int(legend_args[3])
    }

  xlim = None
  if args.xlim:
    xlim = np.array([float(d) for d in args.xlim.split(',')])

  ylim = None
  if args.ylim:
    ylim = np.array([float(d) for d in args.ylim.split(',')])

  bar_chart(
    column_labels,
    row_labels,
    data,
    expected=expected,
    title=args.title,
    xlabel=args.xlabel,
    ylabel=args.ylabel,
    size=size,
    legend=legend,
    xlim=xlim,
    ylim=ylim
  )


if __name__ == '__main__':
  main()