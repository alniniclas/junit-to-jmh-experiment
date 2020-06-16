import itertools

class Result:
  def __init__(self, throughput=None, errors=None):
    self.throughput = throughput if throughput else []
    self.errors = errors if errors else []

  @staticmethod
  def merge(results):
    throughput = []
    errors = []
    for result in results:
      throughput.extend(result.throughput)
      errors.extend(result.errors)
    return Result(throughput=throughput, errors=errors)


class ExperimentResult:
  def __init__(self, batch, repetition, test, runner, result):
    self.batch = batch
    self.repetition = repetition
    self.test = test
    self.runner = runner
    self.result = result


class ExperimentResults:
  def __init__(self, config, data):
    self.config = config
    self._data = data

  @staticmethod
  def from_results(config, experiment_results):
    batches = {}
    for result in experiment_results:
      tests = batches.setdefault(result.batch, {})
      runners = tests.setdefault(result.test, {})
      repetitions = runners.setdefault(result.runner, {})
      repetitions[result.repetition] = result.result
    return ExperimentResults(config, batches)

  def get_results(self, batch=None, repetition=None, test=None, runner=None, combine_repetitions=False):
    results = []
    def filtered_keys(d, filter):
      if filter is not None:
        return (filter,) if filter in d else ()
      else:
        return sorted(d.keys())
    for b in filtered_keys(self._data, batch):
      tests = self._data[b]
      for t in filtered_keys(tests, test):
        runners = tests[t]
        for rn in filtered_keys(runners, runner):
          repetitions = runners[rn]
          if combine_repetitions:
            runner_results = (repetitions[rp] for rp in filtered_keys(repetitions, repetition))
            results.append(ExperimentResult(b, None, t, rn, Result.merge(runner_results)))
          else:
            for rp in filtered_keys(repetitions, repetition):
              results.append(ExperimentResult(b, rp, t, rn, repetitions[rp]))
    return results
