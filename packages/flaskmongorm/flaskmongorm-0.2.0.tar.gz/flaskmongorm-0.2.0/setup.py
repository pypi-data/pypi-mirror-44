"""
flaskmongorm
--------------

simple wrapper for flask-pymongo
"""
from pathlib import Path
from setuptools import setup

p = Path(__file__) / "../flaskmongorm/__init__.py"
with p.resolve().open(encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__ = "):
            version = line.split("=")[-1].strip().replace("'", "")
            break

setup(
    name="flaskmongorm",
    version=version.replace('"', ""),
    url="https://github.com/lixxu/flaskmongorm",
    license="BSD",
    author="Lix Xu",
    author_email="xuzenglin@gmail.com",
    description="Simple wrapper for flask-pymongo",
    long_description=__doc__,
    packages=["flaskmongorm"],
    zip_safe=False,
    platforms="any",
    install_requires=["flask-pymongo", "pytz"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
    ],
)
