from distutils.core import setup

setup(
    name='python-praat-scripts',
    version='0.1.14',
    author='Michael McAuliffe',
    author_email='michael.e.mcauliffe@gmail.com',
    packages=['praatinterface'],
    url='http://pypi.python.org/pypi/python-praat-scripts/',
    license='LICENSE.txt',
    description='Interface for running Praat scripts through Python',
    long_description=open('README.md').read(),
)
