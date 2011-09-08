import os
import itertools
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "snort", "__version__.py")) as version_file:
    exec(version_file.read())

setup(name="snort",
      classifiers = [
          "Programming Language :: Python :: 2.6",
          ],
      description="(Yet another) nosetests growl plugin, using growlnotify",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      install_requires=[],
      scripts=[],
      zip_safe=False,
      namespace_packages=[],
      package_data = {
          '' : ["*.png"],
          },
      entry_points = {
          'nose.plugins' : [
              'snort = snort.nose_plugin:NosePlugin',
              ]
          }
      )
