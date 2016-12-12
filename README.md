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

Low-lever clients, such as the popular 
[`netcat`](https://en.wikipedia.org/wiki/Netcat), are better suited for this 
job.

However, the syntax of HTTP requires headers to be separated with 
`\r\n` which makes it difficult to produce them on the command line. 
A typical solution involves the use of `echo`:


```bash
$ echo -ne 'GET / HTTP/1.1\r\nContent-Length: 5\r\n\r\nhello' | \
    nc localhost 8000
```

`httpcat` makes this easier.


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
$ httpcat | nc httpbin.org 80
POST /post HTTP/1.1
-> POST /post HTTP/1.1\r\n
Host: httpbin.org
-> Host: httpbin.org\r\n
Content-Length: 6
-> Content-Length: 6\r\n

-> \r\n [headers written]
Hello
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Mon, 12 Dec 2016 13:47:16 GMT
Content-Type: application/json
Content-Length: 230
Connection: keep-alive
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {},
  "data": "Hello\n",
  "files": {},
  "form": {},
  "headers": {
    "Content-Length": "6",
    "Host": "httpbin.org"
  },
  "json": null,
  "origin": "89.103.111.135",
  "url": "http://httpbin.org/post"
}
```

Specify headers and body on the command line. 
Note that the omitted `HTTP-Version` is auto-completed:

```bash
$ httpcat 'POST /post' 'Host: httpbin.org' 'Content-Length: 5' '' 'Hello'  | nc httpbin.org 80
-> POST /post HTTP/1.1\r\n
-> Host: httpbin.org\r\n
-> Content-Length: 5\r\n
-> \r\n [headers written]
```

Specify headers and body on the command line. 
Note that the omitted `Method` is set to `GET` and `HTTP-Version` 
is auto-completed:

```bash
$ httpcat '/' 'Host: example.org' ''  | nc example.org 80
-> GET / HTTP/1.1\r\n
-> Host: example.org\r\n
-> \r\n [headers written]
```

### Dependencies

* Python 3


### Installation


```bash
pip3 install httpcat
```

Alternatively, you can just download `httpcat.py` manually and invoke 
it as `./httpcat.py` instead of `httpcat`. 


### Tests

```bash
python3 setup.py test
```
