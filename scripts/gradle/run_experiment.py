import argparse
import json
import os
import time
import re
import subprocess
import xml.etree.ElementTree
import shutil


def load_progress(progress_file, progress_backup_file):
  if os.path.exists(progress_backup_file):
    if os.path.exists(progress_file):
      os.remove(progress_file)
    os.rename(progress_backup_file, progress_file)
  if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
      return json.load(f)
  else:
    return { 'test_index': -1 }


def save_progress(progress_file, progress_backup_file, progress):
  if os.path.exists(progress_file):
    os.rename(progress_file, progress_backup_file)
  with open(progress_file, 'w') as f:
    json.dump(progress, f)
    f.flush()
    os.fsync(f.fileno())
  if os.path.exists(progress_backup_file):
    os.remove(progress_backup_file)


def ju2jmh_benchmark_regex(class_name, test_name):
  regex = re.escape(class_name)
  regex += re.escape('._Benchmark')
  regex += r'(?:_\d+)?'
  regex += re.escape('.benchmark_')
  regex += re.escape(test_name)
  return '^{}$'.format(regex)


def ju4runner_benchmark_regex(class_name, test_name):
  regex = re.escape('{}_JU4Benchmark.benchmark_{}'.format(class_name, test_name))
  return '^{}$'.format(regex)


def jmh_benchmark_command(jar, forks, time, benchmark_type, output_dir, regex):
  time_ms = '{:d}ms'.format(time)
  benchmark_name = '{}-f{:d}-t{:d}'.format(benchmark_type, forks, time)
  return [
    'java', '-jar', jar,
    '-f', str(forks),
    '-w', time_ms,
    '-r', time_ms,
    '-foe', 'true',
    '-rf', 'json',
    '-rff', os.path.join(output_dir, '{}.json'.format(benchmark_name)),
    regex
  ]


def get_test_runtime(project, test_class, test_name):
  results_file = os.path.join(
    project, 'build', 'test-results', 'test', 'TEST-{}.xml'.format(test_class)
  )
  test_cases = xml.etree.ElementTree.parse(results_file).getroot().findall('testcase')
  for test_case in test_cases:
    if test_case.get('name') == test_name:
      return test_case.get('time')


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  args = parser.parse_args()
  
  with open(args.config, 'r') as f:
    config = json.load(f)
  print(config)
  with open(config['test_list'], 'r') as f:
    tests = json.load(f)
  dry_run = False
  if 'dry_run' in config and config['dry_run']:
    dry_run = True

  main_project = os.path.abspath(config['main_project'])
  main_project_gradle = os.path.join(
    main_project, 'gradlew.bat' if os.name == 'nt' else 'gradlew'
  )
  ju2jmh_benchmarks_jar = os.path.abspath(config['ju2jmh_benchmarks_jar'])
  ju4runner_benchmarks_jar = os.path.abspath(config['ju4_runner_benchmarks_jar'])

  output_dir = os.path.abspath(config['output_dir'])
  os.makedirs(output_dir, exist_ok=True)
  progress_file = os.path.join(output_dir, 'progress.json')
  progress_backup_file = os.path.join(output_dir, 'progress.json.old')
  progress = load_progress(progress_file, progress_backup_file)
  last_save = time.monotonic()
  for index in range(progress['test_index'] + 1, len(tests)):
    test = tests[index]

    unit_test = '{}.{}'.format(test['class'], test['test'])
    unit_test_command = [main_project_gradle, 'test', '--tests', unit_test]

    test_temp_dir = os.path.join(output_dir, 'tmp_{:d}'.format(index))
    for repetition in range(config['repetitions']):
      run_id = '[{:d}]{}:{:d}'.format(index, unit_test, repetition)
      repetition_dir = os.path.join(test_temp_dir, str(repetition))

      ju2jmh_benchmark = ju2jmh_benchmark_regex(test['class'], test['test'])
      ju2jmh_benchmark_commands = [
          jmh_benchmark_command(
            ju2jmh_benchmarks_jar, c['forks'], c['time'],
            'ju2jmh', repetition_dir, ju2jmh_benchmark
          )
          for c in config['jmh_configs']
      ]

      ju4runner_benchmark = ju4runner_benchmark_regex(test['class'], test['test'])
      ju4runner_benchmark_commands = [
          jmh_benchmark_command(
            ju4runner_benchmarks_jar, c['forks'], c['time'],
            'ju4runner', repetition_dir, ju4runner_benchmark
          )
          for c in config['jmh_configs']
      ]
      if not dry_run:
        if os.path.exists(repetition_dir):
          shutil.rmtree(repetition_dir)
        os.makedirs(repetition_dir)
      print('{}: subprocess.run({}, cwd={})'.format(run_id, json.dumps(unit_test_command, indent=2), main_project))
      if not dry_run:
        t = time.monotonic() + (config['junit_time'] / 1000.0)
        runtimes = []
        while time.monotonic() < t:
          subprocess.run(
            unit_test_command, cwd=main_project,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
          )
          runtimes.append(get_test_runtime(main_project, test['class'], test['test']))
        with open(os.path.join(repetition_dir, 'unit-test.json'), 'w') as f:
          json.dump({'class': test['class'], 'test': test['test'], 'durations': runtimes}, f, indent=4)
      for command in ju2jmh_benchmark_commands:
        print('{}: subprocess.run({})'.format(run_id, json.dumps(command, indent=2)))
        if not dry_run:
          subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      for command in ju4runner_benchmark_commands:
        print('{}: subprocess.run({})'.format(run_id, json.dumps(command, indent=2)))
        if not dry_run:
          subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    class_output_dir = os.path.join(output_dir, test['class'])
    test_output_dir = os.path.join(class_output_dir, test['test'])
    if not dry_run:
      if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)
      os.makedirs(class_output_dir, exist_ok=True)
      moved_dir_name = shutil.move(test_temp_dir, class_output_dir)
      os.rename(moved_dir_name, test_output_dir)
    progress['test_index'] = index
    if time.monotonic() > last_save + 1:
      save_progress(progress_file, progress_backup_file, progress)
      last_save = time.monotonic()
  save_progress(progress_file, progress_backup_file, progress)


if __name__ == '__main__':
  main()
