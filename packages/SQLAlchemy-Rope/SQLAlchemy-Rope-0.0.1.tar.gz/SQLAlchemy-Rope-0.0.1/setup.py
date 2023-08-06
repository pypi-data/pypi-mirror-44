"""
SQLAlchemy-Rope
-----------
This module provides easy wrapper for thread-local SQLAlchemy session
"""

from setuptools import setup
from os import path

about = {}
with open("sqlalchemy_rope/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      packages=["sqlalchemy_rope"],
      zip_safe=False,
      platforms="any",
      install_requires=["SQLAlchemy"],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ])
