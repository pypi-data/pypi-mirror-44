# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from datetime import timedelta
import re

HOURS = "h"
MINUTES = "m"
SECONDS = "s"
MILLISECONDS = "ms"
WEEKS = "w"
DAYS = "d"

SUFFIXES = [
    ("weeks", WEEKS),
    ("days", DAYS),
    ("hours", HOURS),
    ("minutes", MINUTES),
    ("seconds", SECONDS),
    ("miliseconds", MILLISECONDS),
]

REGEX = "^" +"".join((
    "((?P<{}>\d+?){})?".format(key, suffix)
    for key, suffix in SUFFIXES)) + "$"
REGEX = re.compile(REGEX)

def usage():
    return "".join((
        "<{}>{}".format(key, suffix)
        for key, suffix in SUFFIXES
    ))

def parser(timedelta_stg):
    parts = REGEX.match(timedelta_stg)
    if not parts:
        raise ValueError("Invalid timedelta string")
    parts = parts.groupdict()
    time_params = dict()
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

def main():
    tests = [
        "1s",
        "1h10s",
        "3d",
        "5h",
        "4m",
        "5w4d",
        "1y3d",
    ]

    print usage()
    for test in tests:
        print parser(test)


if __name__ == "__main__":
    main()
