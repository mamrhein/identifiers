# coding=utf-8
"""Setup package 'identifiers'."""

from setuptools import setup, find_packages


with open('README.md') as file:
    long_description = file.read()

setup(
    name="identifiers",
    author="Michael Amrhein",
    author_email="michael@adrhinum.de",
    url="https://github.com/mamrhein/identifiers",
    description="International Standard Identifiers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["iso3166"],
    license='BSD',
    keywords='identifier GS1 GLN GTIN SSCC GSIN ISBN ISMN ISSN BIC IBAN MIC '
             'ISIN VAT',
    platforms='all',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
