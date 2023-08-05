#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2019 Etienne Robillard <tkadm30@yandex.com>
# All rights reserved.
# See NOTICE file for details.

from functools import wraps

from .django_compat import reverse

__all__ = ('permalink', )

def permalink(view_func):
    """
    Decorator that calls urlresolvers.reverse() to return a URL using
    parameters returned by the decorated function "func".

    "view_func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)
    """
    @wraps(view_func)
    def inner(*args, **kwargs):
        bits = view_func(*args, **kwargs)
        return reverse(bits[0], None, *bits[1:3])
    return inner

