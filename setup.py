#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'test': [
        "pytest>=4.4.0",
        "pytest-xdist",
        "tox>=2.9.1,<3",
    ],
    'lint': [
        'black>=19.3b0,<20',
        'flake8>=3.7.0,<4',
        'isort>=4.3.17,<5',   
        'mypy<0.800',
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
}

extras_require['dev'] = (
    extras_require['dev'] +
    extras_require['test'] +
    extras_require['lint'] +
    extras_require['doc']
)

setup(
    name='pytest-ethereum',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='0.1.3-alpha.6',
    description="""pytest-ethereum: Pytest library for ethereum projects.""",
    long_description_markdown_filename='README.md',
    author='pytest-ethereum-contributors',
    author_email='',
    url='https://github.com/ethereum/pytest-ethereum',
    include_package_data=True,
    install_requires=[
        "eth-utils>=1.4.0,<2.0.0",
        "ethpm>=0.1.4a14,<1.0.0",
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    entry_points={"pytest11": ["pytest_ethereum = pytest_ethereum.plugins"]},
    py_modules=['pytest_ethereum'],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
