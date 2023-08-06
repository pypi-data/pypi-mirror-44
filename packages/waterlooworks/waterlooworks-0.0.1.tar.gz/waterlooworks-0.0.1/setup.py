import os
from setuptools import setup

# Taken from https://github.com/kennethreitz/setup.py/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='waterlooworks',
    version='0.0.1',
    description='Package and scripts for interacting with Waterloo Works',
    url='https://github.com/dang3r/waterlooworks',
    author='Daniel Cardoza',
    author_email='dan@danielcardoza.com',
    license='MIT',
    packages=['waterlooworks'],
    python_requires='>=3.4.0',
    scripts=['bin/waterlooworks', 'bin/waterlooworks-grep'],
    install_requires=['click==7.0', 'textmining', 'pdfrw'],
    long_description='\n' + open(os.path.join(here, 'README.md')).read(),
    long_description_content_type='text/markdown',
    zip_safe=False
)
