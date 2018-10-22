"""Main runner for OpenFaaS function"""
# Copyright (c) Nick McClendon 2018. All rights reserved.
# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import json
import os
import sys
from function import handler

def get_stdin():
    """Get all input from stdin"""
    buf = ""
    while True:
        line = sys.stdin.readline()
        buf += line
        if line == "":
            break
    return buf

if __name__ == "__main__":
    st = get_stdin()
    options = json.loads(st)
    ret = handler.handle(options)
    meta = {
        'index': {
            '_index': os.getenv('ELASTIC_INDEX', 'openfaas'),
            '_type': os.getenv('ELASTIC_TYPE', 'result'),
        }
    }
    es = []
    if ret != None:
        for r in ret:
            es.append(meta)
            es.append(r)
        print('\n'.join(json.dumps(e) for e in es))
