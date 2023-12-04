import os
import re

from setuptools import find_namespace_packages, setup

name = 'django-ows-lib'
package = 'ows_lib'
description = 'Well layered ows lib with a client implementation to communicate with ogc services with django based objects, including xml mapper classes to serialize and deserialize ows xml files, such as capabilities.'
url = 'https://github.com/mrmap-community/django-ows-lib'
author = 'mrmap-community'
author_email = 'jonas.kiefer@live.com'
license = 'MIT'


REQUIREMENTS = [
    "django>=3.0",
    "django-axis-order>=0.1.0",
    "eulxml>=1.1.3",
    "isodate>=0.6.1",
    "camel-converter>=3.0.0",
    "requests>=2.23.0",
    "pygeofilter>=0.2.1",
    "pygml>=0.2.2"
]

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


version = get_version(package)

setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author=author,
    author_email=author_email,
    packages=[p for p in find_namespace_packages(
        exclude=('tests*',)) if p.startswith(package)],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
