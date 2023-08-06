#!/usr/bin/env python3
# ==================================================================== #
# -*- coding: utf-8 -*-
#
# IDNA domain names codec
#
# Copyright 2019, Philippe Grégoire <pg@pgregoire.xyz>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
# ==================================================================== #

import socket

# -------------------------------------------------------------------- #

#
# not properly displaying in browsers
#
mutations = {
    # u'\u0251'
    #0430 breaks on chrome
    'a': [u'\u03b1', u'\u0430'],
    'b': [u'\u042c'],
    'c': [u'\u03f2', u'\u0441'],
    'd': [u'\u010f'],
    'e': [u'\u0435'],
    'h': [u'\u04bb'],
    'i': ['ì', 'î', 'ï', u'\u0456'],
    'j': [u'\u0458', u'\u0575'],
    'l': [u'\u04cf'],
    'o': [u'\u03bf', u'\u043e'],
    'p': [u'\u0440'],
    's': [u'\u0455'],
    'y': [u'\u0443'],
    '/': [u'\u2044'],
}

# -------------------------------------------------------------------- #

def isavail(d):
    try:
        return socket.getaddrinfo(d, 80)
    except socket.gaierror:
        return None

# -------------------------------------------------------------------- #

def walk(l, a=[]):
    if not l:
        return a

    if not a:
        a = l[0][::]
    else:
        r = []
        for s in a:
            for c in l[0]:
                r.append(s + c)
        a = r[::]

    return walk(l[1:], a)

# -------------------------------------------------------------------- #

def transform(name):
    n = list(name)

    k = mutations.keys()
    l = []
    for c in name:
        if c not in k:
            l += [[c]]
        else:
            l += [[c] + mutations[c]]

    for d in walk(l):
        yield (d, d.encode('idna').decode('ascii'))

# -------------------------------------------------------------------- #

def decode(domain):
    return domain.encode('utf-8').decode('idna')

# -------------------------------------------------------------------- #

def encode(domain):
    s  = domain.split('.')
    p, e = ('.', []) if 1 != len(s) else ('', [''])
    s += e

    s  = s[-2:]
    d  = p.join(s)

    print('==> {}'.format(d))
    for t in transform(s[0]):
        yield tuple([p.join([t[i], s[1]]) for i in [0,1]])

# ==================================================================== #
