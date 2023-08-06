# decode-datastore-client

This library contains a minimal client library developed as part of the DECODE
project in order to provide a Python client for the encrypted datastore
component.

The purpose of this library is to enable a Python based client application to
easily read from and write to the datastore.

The datastore API is implemented using a simple RPC framework called
[Twirp](https://github.com/twitchtv/twirp). This framework uses protocol
buffers as a transport layer, and provides a suite of tools for generating
server stubs as well as client bindings in a number of programming languages
and can be thought of as being akin to a simpler version of
[GRPC](https://grpc.io).

## Documentation

Documentation for this library has been published to:
https://decode-datastore-client.readthedocs.io/en/latest/

Please have a look there for some more detailed installation instructions and
usage examples.
