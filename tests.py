from httpcat import httpcat, EOF, CRLF


class MockIO:
    def __init__(self, input_lines):
        self.input_lines = iter(input_lines)
        self.output_lines = []

    def readline(self):
        return next(self.input_lines)

    def write(self, line):
        self.output_lines.append(line)

    def flush(self):
        pass


def process(input_lines):
    io = MockIO(input_lines=input_lines)
    httpcat(initial_lines=[], infile=io, outfile=io)
    return io.output_lines


EXPECTED_OUTPUT_LINES = [
    'GET / HTTP/1.1' + CRLF,
    'Content-Type: text/plain' + CRLF,
    CRLF,
    'body',
]


def test_crlf_autocomplete():
    assert EXPECTED_OUTPUT_LINES == process([
        'GET / HTTP/1.1',
        'Content-Type: text/plain',
        '',
        'body',
        EOF,
    ])


def test_method_autocomplete():
    assert EXPECTED_OUTPUT_LINES == process([
        '/ HTTP/1.1',
        'Content-Type: text/plain',
        '',
        'body',
        EOF,
    ])


def test_http_version_autocomplete():
    assert EXPECTED_OUTPUT_LINES == process([
        'GET /',
        'Content-Type: text/plain',
        '',
        'body',
        EOF,
    ])


def test_method_and_http_version_autocomplete():
    assert EXPECTED_OUTPUT_LINES == process([
        '/',
        'Content-Type: text/plain',
        '',
        'body',
        EOF,
    ])
