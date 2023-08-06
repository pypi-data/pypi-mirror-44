import io
import os
import re
import sys

from .pdf_redactor import RedactorOptions, redactor

import waterlooworks as ww

default_options = [
    (
		re.compile(r"(mailto:)?\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+", re.IGNORECASE),
		lambda m: "EMAIL"
	),
	(
		re.compile(r"\s(he|she)\s"),
		lambda m : "they"
	),
    (
		re.compile(r"\s(him|her)\s"),
		lambda m : "them"
	)
]


def anonymize(package, output_dir: str):
	"""Anonymize a package and output it to a directory"""
	name_swap = [(
		re.compile(package.name, re.IGNORECASE),
		lambda m : "STUDENTNAME"
	)]
	options = RedactorOptions()
	options.content_filters = default_options + name_swap
	options.input_stream = open(package.filename, 'rb')
	os.makedirs(output_dir, exist_ok=True)
	filename = os.path.basename(package.filename)
	options.output_stream = io.FileIO(f'{output_dir}/{filename}', mode='w')
	redactor(options)
