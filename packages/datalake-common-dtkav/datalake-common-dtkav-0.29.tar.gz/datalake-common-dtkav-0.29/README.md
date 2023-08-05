[![Build Status](https://travis-ci.org/planetlabs/datalake-common.svg?branch=master)](https://travis-ci.org/planetlabs/datalake-common)

Introduction
============

A datalake is an archive that contains files and metadata records about those
files. datalake-common is a place for code and specification shared by the
handful of components that form the datalake. Mostly, datalake-common is about
defining and validating the schemas that are shared between these components.

Installation
============

For basic metadata handling, just:

        pip install datalake-common


Datalake Metadata
=================

Files that are shipped to the datalake are accompanied by a JSON metadata
document. Here it is:

        {
            "version": 0,
            "start": "2018-05-23T00:00:00.000000Z",
            "end": "2018-05-23T01:02:03.456890Z",
            "path": "/var/log/syslog.1"
            "work_id": null,
            "where": "webserver02",
            "what": "syslog",
            "uuid": " d0b566e9-f780-45f1-81f6-33432cf51b00 ",
            "cid": "bqlsaeecof2h7x7wf32ys3r5ky6jk332k"
        }

version: This is the metadata version. It should be 0.

start: This is the UTC time of the first event in the file. It is an iso8601
datetime. It must use the 'T' separator, include microseconds, and use the 'Z'
time-zone format. Alternatively, if the file is associated with an instant,
this is the only relevant time. It is required.

end: This is the UTC time of the last event in the file. It is an iso8601
datetime. It must use the 'T' separator, include microseconds, and use the 'Z'
time-zone format. If the key is not present or if the value is `None`, the
file represents a snapshot of something like a weekly report where only one
date (`start`) is relevant.

path: The absolute path to the file in the originating filesystem.

where: This is the location or server that generated the file. It is required
and must only contain lowercase alpha-numeric characters, - and _. It should be
concise. 'localhost' and 'vagrant' are bad names. Something like
'whirlyweb02-prod' is good.

what: This is the process or program that generated the file. It is required
and must only contain lowercase alpha-numeric characters, - and _. It must not
have trailing file extension (e.g., .log). The name should be concise to limit
the chances that it conflicts with other whats in the datalake. So names like
'job' or 'task' are bad. Names like 'balyhoo-source-audit' or
'rawfood-ingester' are good.

uuid: A UUID4 for the file assigned by the datalake. It is required.

cid: A base32-encoded 16-byte blake2 hash of the file content. This is
calcluated and assigned by the datalake. It uses mutlibase and multihash, so
is self-describing. It is required.

work_id: This is an application-specific id that can be used later to retrieve
the file. It is required but may be null. In fact the datalake utilities will
generally default it to null if it is not set. It must not be the string
"null". It should be prepended with a domain-specific prefix to prevent
conflicts with other work id spaces. It must only contain lowercase
alpha-numeric characters, -, and _.

Developer Setup
===============

        mkvirtualenv datalake # Or however you like to manage virtualenvs
        pip install -e .[test]
        py.test
