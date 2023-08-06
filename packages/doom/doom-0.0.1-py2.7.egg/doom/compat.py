#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mostly py2/py3 compatibility code; small things that didn't make it into `six`.
"""
__all__ = [
    "unicode", "PY3", "urlparse", "unescape", "ensure_unicode", "ensure_bytes"
]

import six
from six import PY3
from six import text_type as unicode

import six.moves.urllib_parse as urlparse
# Note that urlencode is present in this version of urlparse but
#  not in the one you get from "import urlparse" ... this might be
#  very-version-specific

if PY3:  # pragma: no cover
    import html
    unescape = html.unescape
else:  # pragma: no cover
    html_parser = six.moves.html_parser.HTMLParser()
    unescape = html_parser.unescape


# TODO: should default to utf-8 or ascii?
def ensure_unicode(x, encoding='ascii'):
    """
    Decode bytes to unicode if necessary.

    Parameters
    ----------
    obj : bytes or unicode
    encoding : str, default "ascii"

    Returns
    -------
    unicode
    """
    if isinstance(x, bytes):
        return x.decode(encoding)
    return x


def ensure_bytes(obj, encoding='ascii'):
    """
    Encode unicode to bytes if necessary.

    Parameters
    ----------
    obj : bytes or unicode
    encoding : str, default "ascii"

    Returns
    -------
    bytes
    """
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    return obj
