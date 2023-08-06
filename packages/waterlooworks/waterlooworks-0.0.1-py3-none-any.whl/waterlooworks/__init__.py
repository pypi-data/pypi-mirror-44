#!/usr/bin/env python3

from collections import Counter
import os
import re
import sys

from tika import parser
import click

from .anon import anonymize

def rm_leading_whitespace(text: str):
    """Remove leading whitespace from a string"""
    for i, t in enumerate(text):
        if t.strip() != '':
            return text[i:]

def is_float(val):
    try:
        float(val)
        return True
    except Exception:
        return False

evaluation_keys = ['MARGINAL', 'SATISFACTORY', 'GOOD', 'VERY GOOD', 'EXCELLENT', 'OUTSTANDING']
evaluation_set = set(evaluation_keys)

class Package:
    """A class containing information about a WaterlooWorks student package"""
    columns = ['name', 'year', 'student_id', 'program', 'evaluations', 'averages']

    def __init__(self, filename: str):
        self.filename = filename
        parsed = rm_leading_whitespace(parser.from_file(filename)['content'])
        self.text = parsed.split('\n')
        self.name = self.text[4]
        self.student_id = self.text[6]
        self.program = self.text[8]
        self.year = self.program[:2]

        # Extract coop evaluations
        r = []
        for t in self.text:
            r.extend([ev for ev in evaluation_keys if ev in t])
        self.evaluations = dict(Counter(r))

        # Extract term averages
        p = re.compile('^Term Average: Decision:(\d+(\.\d*)?)')
        avgs = []
        for t in self.text:
            m = p.match(t)
            if m:
                avgs.append(float(m.groups()[0]))
        self.averages = avgs

    def __iter__(self):
        return (getattr(self, col) for col in self.columns)

    def __str__(self):
        return str(list(self))

# Example scoring functions

def grade_score(pkg: Package):
    """Calculate the package average"""
    avgs = [float(avg) for avg in pkg.averages if is_float(avg)]
    return sum(avgs) / len(avgs) if avgs else 0

def eval_score(pkg: Package):
    """Calculate the score based on coop evaluations"""
    score = [pkg.evaluations.get(evaluation, 0) for evaluation in evaluation_keys]
    return tuple(score[::-1])

def agg_score(pkg: Package):
    """Calculate the score using the student year, grade and eval scores"""
    return (pkg.year, grade_score(pkg), eval_score(pkg))

def weighted_eval_score(pkg: Package):
    """Calculate the scores using weighted evaluations"""
    scores = [evaluation_keys.index(evl) * count for evl, count in pkg.evaluations.items()]
    return sum(scores) / (evaluation_keys.index('OUTSTANDING') * len(scores)) if scores else 0
