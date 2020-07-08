import argparse
import pickle
import collections
import matplotlib.pyplot as plt
import numpy as np


from batched_experiment.experiment_statistics import ThroughputStatistics


DataSeries = collections.namedtuple('DataSeries', ('name', 'datapoints'))


def violin_plot(dataset, title=None, xlabel=None, ylabel=None, plot_outliers=True, outlier_jitter=0.0):
  fig, ax = plt.subplots()
  if title:
    ax.set_title(title)
  if xlabel:
    ax.set_xlabel(xlabel)
  if ylabel:
    ax.set_ylabel(ylabel)
  tick_positions = np.arange(1, len(dataset) + 1)
  ax.set_xticks(tick_positions)
  ax.set_xticklabels(series.name for series in dataset)
  datapoints = np.array([series.datapoints for series in dataset])
  mins, q1, medians, q3, maxes = np.percentile(datapoints, [0, 25, 50, 75, 100], axis=1)
  ax.scatter(tick_positions, medians, marker='o', color='white', s=30, zorder=3)
  ax.vlines(tick_positions, q1, q3, color='k', lw=5)
  iqr = q3 - q1
  whiskers_min = q1 - 1.5 * iqr
  whiskers_max = q3 + 1.5 * iqr
  ax.vlines(
    tick_positions,
    [datapoints[i][datapoints[i] >= whiskers_min[i]].min() for i in range(len(datapoints))],
    [datapoints[i][datapoints[i] <= whiskers_max[i]].max() for i in range(len(datapoints))],
    color='k',
    lw=1
  )
  if plot_outliers:
    outlier_ticks = []
    outlier_values = []
    for i in range(len(datapoints)):
      outliers = datapoints[i][(datapoints[i] < whiskers_min[i]) | (datapoints[i] > whiskers_max[i])]
      outlier_ticks.extend((1 * np.random.rand(len(outliers)) - 0.5) * outlier_jitter + tick_positions[i])
      outlier_values.extend(outliers)
    ax.scatter(outlier_ticks, outlier_values, marker='o', c='white', edgecolors='k', s=15, zorder=3)
  plot = ax.violinplot(datapoints.transpose(), showextrema=False)
  for pc in plot['bodies']:
    pc.set_edgecolor('black')
    pc.set_alpha(1)
  plt.show()
