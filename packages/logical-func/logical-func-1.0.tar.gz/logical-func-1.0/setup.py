from setuptools import setup, find_packages

from logical import __version__

extra_test = [
    'pytest>=4',
    'pytest-runner>=4',
    'pytest-cov>=2',
]
extra_dev = extra_test

extra_ci = extra_test + [
    'python-coveralls',
]

setup(
    name='logical-func',

    version=__version__,

    install_requires=[
        'gimme_cached_property',
    ],

    extras_require={
        'test': extra_test,
        'dev': extra_dev,

        'ci': extra_ci,
    },

    packages=find_packages(),

    url='https://github.com/MichaelKim0407/logical-func',

    license='MIT',

    author='Michael Kim',
    author_email='mkim0407@gmail.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Software Development :: Libraries',
    ],
)
