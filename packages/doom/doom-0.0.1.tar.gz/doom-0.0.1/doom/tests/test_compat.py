#!/usr/bin/env python
# -*- coding: utf-8 -*-

from six import text_type as unicode
import pytest

from doom.compat import ensure_unicode, ensure_bytes


def test_ensure_unicode():
    res = ensure_unicode(u'foo')
    assert isinstance(res, unicode)

    # passing encoding=ascii in this case doesn't matter
    res = ensure_unicode(u'£', 'ascii')
    assert isinstance(res, unicode)

    # utf-8 encoding GBP symbol
    res = ensure_unicode(b'\xc2\xa3', 'utf-8')
    assert res == u'£' and isinstance(res, unicode)

    with pytest.raises(UnicodeDecodeError):
        ensure_unicode(b'\xc2\xa3', 'ascii')
    with pytest.raises(UnicodeDecodeError):
        ensure_unicode(b'\xc2\xa3')

    # for anything other than unicode or bytes, we let it through unchanged
    assert ensure_unicode(4) == 4
    assert ensure_unicode(-5.6) == -5.6


def test_ensure_bytes():
    res = ensure_bytes(u'foo')
    assert isinstance(res, bytes)

    # For encoding to bytes, passing an impossible encoding does matter
    #  (unlike for ensure_unicode above)
    with pytest.raises(UnicodeEncodeError):
        ensure_bytes(u'£', 'ascii')
    with pytest.raises(UnicodeEncodeError):
        ensure_bytes(u'£')

    # utf-8 encoding GBP symbol
    res = ensure_bytes(b'\xc2\xa3', 'utf-8')
    assert res == b'\xc2\xa3' and isinstance(res, bytes)

    # since we already have bytes, passing ascii is harmless
    res = ensure_bytes(b'\xc2\xa3', 'ascii')
    assert res == b'\xc2\xa3' and isinstance(res, bytes)

    # for anything other than unicode or bytes, we let it through unchanged
    assert ensure_bytes(4) == 4
    assert ensure_bytes(-5.6) == -5.6
