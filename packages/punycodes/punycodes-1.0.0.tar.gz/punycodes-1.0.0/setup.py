import os
import setuptools
import time


version = '1.0.0'
if '__DEVEL' in os.environ:
    version += ('.' + str(int(time.time())))


setuptools.setup(
    name='punycodes',
    version=version,
    author='Philippe Grégoire',
    author_email='git@pgregoire.xyz',
    packages=['punycodes',],
    scripts=['bin/punycodes',],
    url='http://pypi.python.org/pypi/punycodes/',
    license='LICENSE',
    description='IDNA codec',
    long_description=open('README.rst').read()
)

