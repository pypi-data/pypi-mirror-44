from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='ezstr',
      version='0.2',
      description='No more tostring boilerplate',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/MichaelVerdegaal/ezstr/archive/0.2.tar.gz',
      author='Michael Verdegaal',
      author_email='michaelverdegaal@hotmail.nl',
      license='MIT',
      packages=['ezstr'],
      zip_safe=False)