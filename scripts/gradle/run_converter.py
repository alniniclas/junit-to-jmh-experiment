import argparse
import subprocess
import os

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('ju2jmh_dir', type=str)
  parser.add_argument('source_project_dir', type=str)
  parser.add_argument('dest_project_dir', type=str)
  parser.add_argument('classes_list', type=str)
  parser.add_argument('--ju4-runner', dest='ju4_runner',
                      action='store_true')
  parser.set_defaults(ju4_runner=False)
  parser.add_argument('--tailored', dest='tailored',
                      action='store_true')
  parser.set_defaults(tailored=False)
  args = parser.parse_args()

  ju2jmh_dir = os.path.abspath(args.ju2jmh_dir)
  source_project_dir = os.path.abspath(args.source_project_dir)
  dest_project_dir = os.path.abspath(args.dest_project_dir)
  classes_file = os.path.abspath(args.classes_list)

  gradlew = os.path.join(ju2jmh_dir, 'gradlew.bat' if os.name == 'nt' else 'gradlew')
  sources_path = os.path.join(source_project_dir, 'src', 'test', 'java')
  classpath = os.path.join(source_project_dir, 'build', 'classes', 'java', 'test')
  dest_sources_dir = os.path.join(dest_project_dir, 'src', 'jmh', 'java')

  converter_args = "'{sources_path}' '{classpath}' '{output_path}' --class-names-file '{classes_list}'".format(
    sources_path=sources_path,
    classpath=classpath,
    output_path=dest_sources_dir,
    classes_list=classes_file
  )
  if args.ju4_runner:
    converter_args = '{} --ju4-runner-benchmark'.format(converter_args)
  if args.tailored:
    converter_args = '{} --tailored-benchmark'.format(converter_args)
  with subprocess.Popen([gradlew, ':converter:run', '--args={}'.format(converter_args)], cwd=ju2jmh_dir) as converter:
    converter.wait()


if __name__ == '__main__':
  main()
