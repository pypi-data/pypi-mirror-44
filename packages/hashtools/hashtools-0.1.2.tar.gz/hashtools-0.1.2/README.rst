hashtools
=========

.. image:: https://travis-ci.org/appstore-zencore/hashtools.svg?branch=master
    :target: https://travis-ci.org/appstore-zencore/hashtools

Hash tools collection, like md5, sha1, sha256 and many other hash tools.


Install
-------

::

    pip install hashtools


Commands
--------

- DSA
- DSA-SHA
- MD4
- MD5
- RIPEMD160
- SHA
- SHA1
- SHA224
- SHA256
- SHA384
- SHA512
- blake2b
- blake2s
- dsaEncryption
- dsaWithSHA
- ecdsa-with-SHA1
- md4
- md5
- ripemd160
- sha
- sha1
- sha224
- sha256
- sha384
- sha3_224
- sha3_256
- sha3_384
- sha3_512
- sha512
- shake_128
- shake_256
- whirlpool

Note:

1. Algorithms above are available in python 3.6.5 on windows 10.
2. In python 2.6, only md5, sha1, sha224, sha256, sha384, sha512 are available.


Usage
-----

::

    C:\Data\hashtools\test>md5 --help
    Usage: MD5 [OPTIONS] [FILES]...

    Options:
    -v, --verbose
    --help         Show this message and exit.

    C:\Data\hashtools\test>sha1 --help
    Usage: SHA1 [OPTIONS] [FILES]...

    Options:
    -v, --verbose
    --help         Show this message and exit.

Example
-------

::

    C:\Data\hashtools\test>echo msg | md5
    b47d94f422d2032dac746f8b6cb263a5

    C:\Data\hashtools\test>echo msg | md5 -v
    b47d94f422d2032dac746f8b6cb263a5 -

    C:\Data\hashtools\test>echo msg | sha256
    c7b6fcf29e713727bdea4c283d816c42cce9a0b4cb08484223f3b9b45256ec59

    C:\Data\hashtools\test>echo msg > a.txt

    C:\Data\hashtools\test>type a.txt
    msg

    C:\Data\hashtools\test>md5 a.txt
    b47d94f422d2032dac746f8b6cb263a5

    C:\Data\hashtools\test>md5 a.txt -v
    b47d94f422d2032dac746f8b6cb263a5 a.txt

