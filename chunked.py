"""Implementation of chunked transfer encoding as defined in RFC 7230."""
from io import DEFAULT_BUFFER_SIZE
from re import compile
from typing import BinaryIO


def encode(dst: BinaryIO, src: BinaryIO) -> None:
    """
    Encodes from the given source and writes chunks to the given destination.
    """
    while True:
        chunk_data = src.read(DEFAULT_BUFFER_SIZE)
        chunk_size = len(chunk_data)

        args = chunk_size, chunk_data
        chunk = b"%X\r\n%s\r\n" % args
        dst.write(chunk)

        if chunk_size == 0:
            break


def decode(dst: BinaryIO, src: BinaryIO) -> None:
    """
    Decodes from the given source and writes chunk contents to the given
    destination.
    """
    while True:
        chunk = src.readline()
        match = _CHUNK_PATTERN.fullmatch(chunk)
        if match is None:
            raise ValueError

        chunk_size_str = match.group("chunk_size")
        chunk_size = int(chunk_size_str, 16)
        if chunk_size == 0:
            break

        while chunk_size > 0:
            buf = src.read(chunk_size)
            dst.write(buf)
            chunk_size -= len(buf)

        crlf = src.readline()
        if _CRLF_PATTERN.fullmatch(crlf) is None:
            raise ValueError

    for line in src:
        if _CRLF_PATTERN.fullmatch(line) is not None:
            return

        if _TRAILER_PART_PATTERN.fullmatch(line) is None:
            raise ValueError


_CHUNK_PATTERN = compile(
    br"(?P<chunk_size>[\dA-F]+)"
    br"(?:"
    br";[-!#$%&'*+.^`|~\w]+"
    br"(?"
    br":=[-!#$%&'*+.^`|~\w]+|\""
    br"(?:[\t !#-\[\]-~\x80-\xFF]|\\[\t \x21-\x7E\x80-\xFF])"
    br"\""
    br")?"
    br")*"
    br"\r\n"
)

_CRLF_PATTERN = compile(b"\r\n")

_TRAILER_PART_PATTERN = compile(
    br"[-!#$%&'*+.^`|~\w]+:[ \t]*"
    br"(?:"
    br"(?:[\x21-\x7E\x80-\xFF](?:[ \t]+[\x21-\x7E\x80-\xFF])?)|(?:\r\n[ \t]+)"
    br")*"
    br"[ \t]*\r\n"
)
