import matplotlib.pyplot as plt
import numpy as np


def bar_chart(
  bar_labels,
  group_labels,
  data,
  expected=None,
  title=None,
  xlabel=None,
  ylabel=None,
  size=None,
  legend=None,
  xlim=None,
  ylim=None
):
  tick_pos = np.arange(len(group_labels))

  width = 0.8 / len(bar_labels)
  bar_pos = 0.8 * ((np.arange(len(bar_labels)) + 0.5) / len(bar_labels) - 0.5)

  fig, ax = plt.subplots()
  if title:
    ax.set_title(title)
  if xlabel:
    ax.set_xlabel(xlabel)
  if ylabel:
    ax.set_ylabel(ylabel)
  for i in range(len(bar_labels)):
    bars = ax.bar(bar_pos[i] + tick_pos, data[i], width, label=bar_labels[i])
    # ax.bar_label(bars, padding=3)
    if expected:
      ax.axhline(expected[i], color=f'C{i}', linestyle='dashed', alpha=0.4)

  ax.set_xticks(tick_pos)
  ax.set_xticklabels(group_labels, rotation=40, ha='right')
  if legend:  
    ax.legend(**legend)
  else:
    ax.legend()

  if size is not None:
    fig.set_size_inches(size / fig.dpi)

  if xlim is not None:
    plt.xlim(xlim)

  if ylim is not None:
    plt.ylim(ylim)

  fig.tight_layout()

  plt.show()
