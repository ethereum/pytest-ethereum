#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)

extras_require = {
    'test': [
        "pytest==3.3.2",
        "pytest-xdist",
        "tox>=2.9.1,<3",
    ],
    'lint': [
        'black>=18.6b4,<19',
        "flake8==3.4.1",
        "isort>=4.2.15,<5",
        "mypy<0.600",
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
    version='0.1.3-alpha.4',
    description="""pytest-ethereum: Pytest library for ethereum projects.""",
    long_description_markdown_filename='README.md',
    author='pytest-ethereum-contributors',
    author_email='',
    url='https://github.com/ethereum/pytest-ethereum',
    include_package_data=True,
    install_requires=[
        "eth-abi>=1.2.2,<2",
        "eth-utils>=1,<2",
        "ethpm>=0.1.4a1,<1",
        'web3[tester]>=4.7,<5',
        "vyper>=0.1.0b5,<1",
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
