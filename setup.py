import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

from httpcat import __author__, __version__, __licence__, __doc__


class PyTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--verbose',
            'tests.py',
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


setup(
    name='httpcat',
    description=__doc__.strip(),
    long_description=open('README.md').read().strip(),
    version=__version__,
    author=__author__,
    author_email='jakub@roztocil.co',
    license=__licence__,
    url='https://github.com/jkbrzt/httpcat',
    download_url='https://github.com/jkbrzt/httpcat',
    py_modules=[
        'httpcat',
    ],
    entry_points={
        'console_scripts': [
            'httpcat = httpcat:main',
        ],
    },
    tests_require=[
        'pytest',
    ],
    cmdclass={
        'test': PyTestCommand
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ],
)
