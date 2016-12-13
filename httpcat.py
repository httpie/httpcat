#!/usr/bin/env python3
"""
Create raw HTTP requests on the command line.

"""
import sys
import argparse
from signal import signal, SIGPIPE, SIG_DFL


__author__ = 'Jakub Roztocil'
__version__ = '0.0.2'
__licence__ = 'BSD'


signal(SIGPIPE, SIG_DFL)


EOF = ''
CRLF = '\r\n'


def httpcat(initial_lines=sys.argv[1:],
            infile=sys.stdin,
            outfile=sys.stdout,
            logfile=sys.stderr,
            verbose=False):

    class sent:
        request_line = False
        headers = False

    def log(msg, prefix='> '):
        if verbose:
            logfile.write(prefix + msg.rstrip() + '\n')
            logfile.flush()

    def write_line(line):
        if not sent.request_line:
            sent.request_line = True
            line = line.strip()
            if line.startswith('/'):
                line = 'GET ' + line
            if 'HTTP/' not in line:
                line += ' HTTP/1.1'
            return write_line(line)
        elif not sent.headers:
            if not line.endswith(CRLF):
                line = line.rstrip() + CRLF
        elif line == EOF:
            return False

        outfile.write(line)
        outfile.flush()

        if sent.headers:
            log(line)
        else:
            log(repr(line).strip("'"))
            if line == CRLF:
                sent.headers = True

        return True

    try:
        for line in initial_lines:
            write_line(line)
        if infile:
            while write_line(infile.readline()):
                pass
    except KeyboardInterrupt:
        pass


parser = argparse.ArgumentParser(
    description=__doc__.strip(),
    epilog='project homepage: https://github.com/jkbrzt/httpcat',

)
parser.add_argument(
    '-V, --version',
    action='version',
    version=__version__,
)
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help='print info about output lines to stderr',
)
parser.add_argument(
    'lines',
    metavar='line',
    nargs=argparse.ZERO_OR_MORE,
    help='input lines read before lines from stdin',
)
parser.add_argument(
    '-n',
    '--no-stdin',
    dest='read_stdin',
    action='store_false',
    default=True,
    help='disable reading of lines from stdin',
)


def main():
    args = parser.parse_args()
    httpcat(
        initial_lines=args.lines,
        infile=sys.stdin if args.read_stdin else None,
        verbose=args.verbose
    )


if __name__ == '__main__':
    main()
