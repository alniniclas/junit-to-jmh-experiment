import json
import os


from functools import total_ordering


@total_ordering
class Test:
  def __init__(self, class_name, method_name):
    self.class_name = class_name
    self.method_name = method_name

  def __eq__(self, other):
    if isinstance(other, Test):
      return (self.class_name, self.method_name) == (other.class_name, other.method_name)
    return NotImplemented

  def __hash__(self):
    return hash((self.class_name, self.method_name))

  def __lt__(self, other):
    return (self.class_name, self.method_name) < (other.class_name, other.method_name)


@total_ordering
class RunnerConfiguration:
  def __init__(self, name, approach):
    self.name = name
    self.approach = approach

  def __eq__(self, other):
    if isinstance(other, RunnerConfiguration):
      return self.name == other.name
    return NotImplemented

  def __hash__(self):
    return hash(self.name)

  def __lt__(self, other):
    return self.name < other.name


class GradleTestRunnerConfiguration(RunnerConfiguration):
  def __init__(self, name, project_root, subproject_path, executions):
    super().__init__(name, 'gradle-test')
    self.project_root = os.path.abspath(project_root)
    self.subproject_path = subproject_path
    self.executions = executions
    self.output_file = '{}_output.json'.format(self.name)


class JmhRunnerConfiguration(RunnerConfiguration):
  def __init__(self, name, approach, jar, forks, time):
    super().__init__(name, approach)
    self.jar = os.path.abspath(jar)
    self.forks = forks
    self.time = time

  def benchmark_output_file(self, test):
    return os.path.join(self.name, test.class_name, test.method_name, 'output.json')


class BatchedExperimentConfiguration:
  @staticmethod
  def _split_into_batches(tests, batch_size):
    return [tests[i:i+batch_size] for i in range(0, len(tests), batch_size)]

  def __init__(self, tests, runner_configs, batch_size, repetitions, output_dir):
    self.test_batches = BatchedExperimentConfiguration._split_into_batches(tests, batch_size)
    self.batch_size = batch_size
    self.repetitions = repetitions
    self.runner_configs = runner_configs
    self.output_dir = os.path.abspath(output_dir)
    self.progress_file = os.path.join(self.output_dir, 'progress.json')
    self.progress_backup_file = os.path.join(self.output_dir, 'progress.json.old')

  def batch_dir(self, batch):
    return os.path.join(self.output_dir, 'b{:d}'.format(batch))

  def repetition_dir(self, batch, repetition):
    return os.path.join(self.batch_dir(batch), 'r{:d}'.format(repetition))

  @staticmethod
  def parse_from_file(config_file):
    with open(config_file, 'r') as f:
      config_dict = json.load(f)

    with open(config_dict['test_list'], 'r') as f:
      test_dicts = json.load(f)

    tests = [Test(td['class'], td['test']) for td in test_dicts]

    def parse_runner_config(runner_config):
      name = runner_config['name']
      approach = runner_config['approach']
      if approach == 'gradle-test':
        project_root = runner_config['project_root']
        subproject_path = runner_config['subproject_path'] if 'subproject_path' in runner_config else []
        executions = runner_config['executions']
        return GradleTestRunnerConfiguration(name, project_root, subproject_path, executions)
      elif approach in ('jmh', 'ju2jmh', 'ju4runner'):
        jar = runner_config['jar']
        forks = runner_config['forks']
        time = runner_config['time']
        return JmhRunnerConfiguration(name, approach, jar, forks, time)
      raise ValueError('Unrecognised approach: {}'.format(approach))

    runner_configs = [parse_runner_config(rcd) for rcd in config_dict['configs']]

    return BatchedExperimentConfiguration(
      tests, runner_configs, config_dict['batch_size'], config_dict['repetitions'], config_dict['output_dir']
    )
