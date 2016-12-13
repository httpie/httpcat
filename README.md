# `httpcat`

[![Build Status](https://travis-ci.org/jkbrzt/httpcat.svg?branch=master)](https://travis-ci.org/jkbrzt/httpcat)

``httpcat`` is a simple utility for constructing raw HTTP
requests on the command line.


## Why?

Sometimes it is useful to be able to create an actual raw 
[HTTP request](https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html)
on the  command line:
 
* To debug a server issue
* To test the handling of invalid HTTP requests
* To learn how HTTP works under the hood

In such cases, existing CLI HTTP clients—such as 
[`httpie`](https://httpie.org),
[`curl`](https://curl.haxx.se/), 
or [`wget`](https://www.gnu.org/software/wget/) 
—are too high-level as they provide
an abstraction layer and one doesn't have a complete control over the 
exact raw data that gets written to the HTTP socket connection.

Lower-level tools, such as the popular 
[`netcat`](https://en.wikipedia.org/wiki/Netcat), are better suited for this 
job.

However, the syntax of HTTP requires headers to be separated with 
`\r\n` which makes it difficult to produce them on the command line. 
A typical solution involves the use of `echo`:


```bash
$ echo -ne 'GET / HTTP/1.1\r\nHost: httpbin.org\r\nContent-Length: 5\r\n\r\nHello' | \
    nc localhost 8000
```

`httpcat` makes this easier:


## How it works

1. Reads command arguments as lines and then lines from ``stdin``
2. Auto-completes them, if necessary
3. Writes them to ``stdout``


## Features

* Automatic ``\r\n`` completion
* Automatic `Method` completion in `Request-Line`
* Automatic `HTTP-Version` completion in `Request-Line`


## Usage

Interactively create a request and send it with `nc`:

```bash
$ httpcat -v | nc httpbin.org 80
POST /post HTTP/1.1
> POST /post HTTP/1.1\r\n
Host: httpbin.org
> Host: httpbin.org\r\n
Content-Length: 6
> Content-Length: 6\r\n

> \r\n
> Hello
```

Specify the whole request in the arguments. Here `''` represents an empty
line which will be converted to `\r\n\` separating the headers and the body.  
Note also that the omitted `HTTP-Version` is auto-completed:

```bash
httpcat -v 'POST /post' 'Host: httpbin.org' 'Content-Length: 5' '' 'Hello'  | nc httpbin.org 80
> POST /post HTTP/1.1\r\n
> Host: httpbin.org\r\n
> Content-Length: 5\r\n
> \r\n
> Hello

```

Specify headers and body on the command line. 
Note that the omitted `Method` is set to `GET` and `HTTP-Version` 
is auto-completed:

```bash
$ httpcat -vn '/' 'Host: example.org' ''  | nc example.org 80
-> GET / HTTP/1.1\r\n
-> Host: example.org\r\n
-> \r\n [headers written]
```

You can, for example, use `stdin` for data and arguments for headers: 

```bash
cat file.txt | httpcat -v 'POST /post' 'Host: httpbin.org' 'Content-Length: 16' '' | nc httpbin.org 80
> POST /post HTTP/1.1\r\n
> Host: httpbin.org\r\n
> Content-Length: 16\r\n
> \r\n
> Hello from file
```

See also `httpcat --help`:

```
usage: httpcat [-h] [-V, --version] [-v] [-n] [line [line ...]]

Create raw HTTP requests on the command line.

positional arguments:
  line            input lines read before lines from stdin

optional arguments:
  -h, --help      show this help message and exit
  -V, --version   show program's version number and exit
  -v, --verbose   print info about output lines to stderr
  -n, --no-stdin  disable reading of lines from stdin
```


## Dependencies

* Python 3


## Installation


```bash
pip3 install httpcat
```

Alternatively, you can just download `httpcat.py` manually and invoke 
it as `./httpcat.py` instead of `httpcat`. 


## Tests

```bash
python3 setup.py test
```

## Changelog


* `0.0.2` (2016-12-13)
    * Added `-v, --verbose` and the command is more quiet by default.
    * Added `-n, --no-stdin`
    * Added `-h, --help` 
    * Added `-V, --version`

* `0.0.1` (2016-12-12)
   * Initial release.
