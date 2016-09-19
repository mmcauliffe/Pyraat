import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

def readme():
    with open('README.md') as f:
        return f.read()

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        if __name__ == '__main__':
            import pytest
            errcode = pytest.main(self.test_args)
            sys.exit(errcode)
setup(
    name = 'python-praat-scripts',
    version = '0.2.2',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic',
      ],
    author = 'Michael McAuliffe',
    author_email = 'michael.e.mcauliffe@gmail.com',
    packages = ['praatinterface'],
    url = 'http://pypi.python.org/pypi/python-praat-scripts/',
    license = 'LICENSE.txt',
    description = 'Interface for running Praat scripts through Python',
    long_description = readme(),
    cmdclass = {'test': PyTest},
    extras_require = {
        'testing': ['pytest'],
    }
)
