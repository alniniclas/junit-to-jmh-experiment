import argparse
import json
import os
import shutil
import subprocess
import time


def load_results(results_file, results_backup):
  if os.path.exists(results_backup):
    if os.path.exists(results_file):
      os.remove(results_file)
    os.rename(results_backup, results_file)
  if os.path.exists(results_file):
    with open(results_file, 'r') as f:
      return json.load(f)
  else:
    return []


def save_results(results, results_file, results_backup):
  if os.path.exists(results_file):
    os.rename(results_file, results_backup)
  with open(results_file, 'w') as f:
    json.dump(results, f, indent=2)
    f.flush()
    os.fsync(f.fileno())
  if os.path.exists(results_backup):
    os.remove(results_backup)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('config', type=str)
  args = parser.parse_args()

  with open(args.config, 'r') as f:
    config = json.load(f)

  results = load_results(config['results_file'], config['results_backup_file'])

  gradlew = os.path.join(config['ju2jmh'], 'gradlew.bat' if os.name == 'nt' else 'gradlew')
  env = os.environ.copy()
  if 'java_options' in config:
    env['_JAVA_OPTIONS'] = config['java_options']

  for i in range(len(results), config['repetitions']):
    print('{:d}/{:d}'.format(i + 1, config['repetitions']))
    output_sources_dir = os.path.join(config['output_sources_root'], str(i))
    if os.path.exists(output_sources_dir):
      shutil.rmtree(output_sources_dir)
    os.mkdir(output_sources_dir)
    converter_args = "'{sources_path}' '{classpath}' '{output_path}' --class-names-file '{classes_list}'".format(
      sources_path=config['sources_root'],
      classpath=config['bytecode_root'],
      output_path=output_sources_dir,
      classes_list=config['test_classes_list']
    )
    print('gradlew :converter:run --args="{}"'.format(converter_args))
    popen_args = [gradlew, ':converter:run', '--args={}'.format(converter_args)]
    start_time = time.monotonic()
    with subprocess.Popen(popen_args, cwd=config['ju2jmh'], env=env) as converter:
      converter.wait()
    end_time = time.monotonic()
    shutil.rmtree(output_sources_dir)
    results.append(end_time - start_time)
    save_results(results, config['results_file'], config['results_backup_file'])


if __name__ == '__main__':
  main()
