#!/usr/bin/env python
from functools import wraps
import os
import public


@public.add
def popd(func):
    """`@popd` decorator. restore previous current directory"""
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            cwd = os.getcwd()
            return func(*args, **kwargs)
        finally:
            os.chdir(cwd)
    return decorated
