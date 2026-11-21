import struct

BOOK_LEN=5

HOST = "localhost"
PORT = 8080

HEADER_FORMAT = "!I"
CLIENT_FORMATS = ["15s", "!3d"]
SERVER_FORMATS = ["15s", "!3d"]

HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CLIENT_SIZE = [struct.calcsize(format) for format in CLIENT_FORMATS]
SERVER_SIZE = [struct.calcsize(format) for format in SERVER_FORMATS]