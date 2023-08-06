
import aioagi

from setuptools import setup, find_packages

README = open('README.rst').read()

tests_require = ['coverage', 'pytest', 'pytest-asyncio', 'async_generator', 'pytest-sugar', 'pytest-cov']


setup(
    name='aioagi',
    version=aioagi.VERSION,
    description='Async agi client/server framework (asyncio)',
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: AsyncIO',
    ],
    author='Shakurov Vadim Vladimirovich',
    author_email='apelsinsd@gmail.com',
    url='https://gitlab.com/VadimShakurov/aioagi.git',
    license='Apache 2',
    keywords='aiogi asyncio asterisk telephony voip',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'aiohttp>=3.4.0,<3.5.0',
    ],
    tests_require=tests_require,
    extras_require={
        'dev': [
            'ipdb',
            'ipython',
        ],
        'testing': tests_require
    },
)
