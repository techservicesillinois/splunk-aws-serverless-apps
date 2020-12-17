#!  /usr/bin/env python3

# import argparse
import os
import sys

#   FIXME: hack
sys.path.insert(0, '..')

print(sys.path)

import splunk

print(dir(splunk))

#const handler = require('../index.js').handler;
#
#let callCount = 0;
#
#function callback(error, count) {
#   console.log("***** END REQUEST", callCount, "*****");
#   if (! error)
#       return;
#
#   console.log(error);
#}
#
#process.stdin.setEncoding('utf8');
#
#process.stdin.on('readable', () => {
#  const chunk = process.stdin.read();
#
#  if (chunk !== null) {
#   callCount++;
#   console.log("===== BEGIN REQUEST", callCount, " =====");
#   const parsed = JSON.parse(chunk.toString('ascii'));
#   // console.log(JSON.stringify(parsed, null, 2));
#   handler(parsed.event, parsed.context, callback);
#  }
#});

#####

def main(argv):
    #   Don't buffer standard output.
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', -1)

#   #   Create top-level parser.
#   parser = argparse.ArgumentParser()
#
#   parser.add_argument \
#       ('--verbose', dest='verbose', action='count', default=0,
#        help='verbosity level')
#
#   #   Parse arguments.
#   arg = parser.parse_args()
#
#   print(arg)

#   #   TODO: See if package name can be autodiscovered.
#   init_logging(level=logging.INFO, addl_loggers=[ 'webdocs_content' ])

    with open('debug-roma.json') as stream:
        print(stream)
    # end with.

    return 0

#####

if __name__ == '__main__':
    sys.exit(main(sys.argv))
