from setuptools import setup, find_packages
import re, os

'''
if os.path.isdir("build"):
    os.rmdir("build")

if os.path.isdir("dist"):
    os.rmdir("dist")

if os.path.isdir("simpleyoutubedata.egg-info"):
    os.rmdir("simpleyoutubedata.egg-info")
'''

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('youtube/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README') as f:
    readme = f.read()

setup(name='simpleyoutubedata',
      author='Katistic',
      version=version,
      packages=find_packages(),
      license='MIT',
      description='Python youtube-api-for-python wrapper',
      long_description=readme,
      long_description_content_type="text/markdown",
      include_package_data=True,
      install_requires=requirements,
      python_requires='>=3.5.3',
      classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Utilities'
      ]
)
