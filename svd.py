#! /usr/bin/env python
# -*- coding: utf-8 -*-
u"""Singular value decomposition
"""
import os
import re
import sys
import argparse
import functools


class Tokenizer(object):
    def __init__(self, *funcs):
        self._funcs = funcs

    def __call__(self, txt):
        words = txt.split()
        for func in self._funcs:
            words = [func(word) for word in words]
        return words


def strip_chr(ch, txt):
    return txt.strip(ch)


class BracketReplace(object):
    def __init__(self):
        self._regx = re.compile('\[.*\]')

    def __call__(self, txt):
        return self._regx.subn('', txt)[0]


def clean_word(txt):
    if len(txt) == 1:
        return ''
    else:
        return txt


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory')
    args = parser.parse_args(argv)
    tokenize = Tokenizer(
        functools.partial(strip_chr, '.'),
        functools.partial(strip_chr, ','),
        functools.partial(strip_chr, ':'),
        functools.partial(strip_chr, ';'),
        BracketReplace(),
        clean_word,
    )
    words = set()
    for entry in os.scandir(args.directory):
        if entry.is_file():
            with open(entry.path, 'rb') as fp:
                txt = fp.read().decode()
                words.update(tokenize(txt))

    words = sorted(words, key=lambda word: len(word), reverse=True)
    records = []

    for entry in os.scandir(args.directory):
        if entry.is_file():
            with open(entry.path, 'rb') as fp:
                buf = fp.read().decode()
                records.append([buf.count(word) for word in words])

    for rec in records:
        print(rec)


if __name__ == '__main__':
    sys.exit(main())
