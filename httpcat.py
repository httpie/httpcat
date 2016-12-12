#!/usr/bin/env python3
"""
Create raw HTTP requests on the command line.

"""
import sys
from signal import signal, SIGPIPE, SIG_DFL


__author__ = 'Jakub Roztocil'
__version__ = '0.0.1'
__licence__ = 'BSD'


signal(SIGPIPE, SIG_DFL)


EOF = ''
CRLF = '\r\n'


def main(initial_lines=sys.argv[1:],
         infile=sys.stdin,
         outfile=sys.stdout,
         logfile=sys.stderr):

    class sent:
        request_line = False
        headers = False

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

        if not sent.headers:
            msg = '-> ' + repr(line).strip("'")
            if line == CRLF:
                msg += ' [headers written]'
                sent.headers = True
            logfile.write(msg + '\n')
            logfile.flush()

        return True

    try:
        for line in initial_lines:
            write_line(line)

        while write_line(infile.readline()):
            pass
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
