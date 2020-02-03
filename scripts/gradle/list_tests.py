import argparse
import os
import xml.etree.ElementTree
import itertools
import random
import json


def get_test_cases(file):
  test_cases =  xml.etree.ElementTree.parse(file).getroot().findall('testcase')
  return ({'class': tc.get('classname'), 'test': tc.get('name')}
          for tc in test_cases if tc.find('skipped') is None)


def get_test_classes(file):
  test_cases =  xml.etree.ElementTree.parse(file).getroot().findall('testcase')
  return frozenset(tc.get('classname') for tc in test_cases if tc.find('skipped') is None)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('input_dir', type=str)
  parser.add_argument('output_file', type=str)
  parser.add_argument('--classes-only', dest='classes_only', action='store_true')
  parser.add_argument('--shuffle-output', dest='shuffle_output', action='store_true')
  parser.add_argument('--plaintext-output', dest='plaintext_output', action='store_true')
  parser.set_defaults(classes_only=False, shuffle_output=False, plaintext_output=False)
  args = parser.parse_args()
  input_dir = os.path.abspath(args.input_dir)
  file_names = (os.path.join(input_dir, fn)
                for fn in os.listdir(input_dir) if fn.endswith('.xml'))
  action = get_test_classes if args.classes_only else get_test_cases
  test_cases = list(itertools.chain.from_iterable(map(action, file_names)))
  if args.shuffle_output:
    random.shuffle(test_cases)
  if not args.plaintext_output:
    with open(args.output_file, 'w') as f:
      json.dump(test_cases, f, indent=4)
  else:
    with open(args.output_file, 'w') as f:
      if not args.classes_only:
        test_cases = ['{}.{}'.format(tc['class'], tc['test']) for tc in test_cases]
      for test_case in test_cases:
        print(test_case, file=f)


if __name__ == '__main__':
  main()
