#!/usr/bin/env python
# Copyright 2017 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


import argparse
import os
import sys
import textwrap

from util import build_utils

SCRIPT_TEMPLATE = textwrap.dedent(
    """\
    #!/usr/bin/env python
    #
    # This file was generated by build/android/gyp/create_stack_script.py

    import os
    import sys

    def main(argv):
      script_directory = os.path.dirname(__file__)
      resolve = lambda p: os.path.abspath(os.path.join(script_directory, p))
      script_path = resolve('{script_path}')
      script_args = {script_args}
      script_path_args = {script_path_args}
      for arg, path in script_path_args:
        script_args.extend([arg, resolve(path)])
      script_cmd = [script_path] + script_args + argv
      print ' '.join(script_cmd)
      os.execv(script_path, script_cmd)

    if __name__ == '__main__':
      sys.exit(main(sys.argv[1:]))
    """)


def main(args):

  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--script-path',
      help='Path to the wrapped script.')
  parser.add_argument(
      '--script-output-path',
      help='Path to the output script.')
  group = parser.add_argument_group('Path arguments')
  group.add_argument('--output-directory')
  group.add_argument('--packed-libs')

  args, script_args = parser.parse_known_args(build_utils.ExpandFileArgs(args))

  def relativize(p):
    return os.path.relpath(p, os.path.dirname(args.script_output_path))

  script_path = relativize(args.script_path)

  script_path_args = []
  if args.output_directory:
    script_path_args.append(
        ('--output-directory', relativize(args.output_directory)))
  if args.packed_libs:
    for p in build_utils.ParseGnList(args.packed_libs):
      script_path_args.append(('--packed-lib', relativize(p)))

  with open(args.script_output_path, 'w') as script:
    script.write(SCRIPT_TEMPLATE.format(
        script_path=script_path,
        script_args=script_args,
        script_path_args=script_path_args))

  os.chmod(args.script_output_path, 0750)

  return 0


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
