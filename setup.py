from setuptools import setup, find_packages


with open('README.TXT') as file:
    long_description = file.read()
with open('CHANGES.TXT') as file:
    long_description += file.read()

setup(
    name="identifiers",
    use_vcs_version=True,
    setup_requires=["hgtools"],
    install_requires=["iso3166"],
    packages=find_packages(),
    author="Michael Amrhein",
    author_email="michael@adrhinum.de",
    url="https://pypi.python.org/pypi/identifiers",
    description="International Standard Identifiers",
    long_description=long_description,
    license='BSD',
    keywords='identifier GS1 GLN GTIN SSCC GSIN ISBN ISMN ISSN BIC IBAN',
    platforms='all',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
