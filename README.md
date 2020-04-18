# httpchunked

Do you need support for chunked transfer encoding in your Python web server,
without adding a dependency on a complete framework? Then `httpchunked` is
the module you need! It has no third-party dependencies and consists of only
two functions: `decode` and `encode`.

## Usage

### Decoding

```sh
$ cat main.py
from io import BytesIO

from httpchunked import decode

if __name__ == "__main__":
    dst = BytesIO()
    src = BytesIO(b"3\r\nfoo\r\n0\r\n\r\n")
    decode(dst, src)
    raw = dst.getvalue()
    print(raw)
$ python main.py
b'foo'
```

### Encoding

```sh
$ cat main.py
from io import BytesIO

from httpchunked import encode

if __name__ == "__main__":
    dst = BytesIO()
    src = BytesIO(b"foo")
    encode(dst, src)
    raw = dst.getvalue()
    print(raw)
$ python main.py
b'3\r\nfoo\r\n0\r\n\r\n'
```

## Installation

```sh
pip install httpchunked
```
