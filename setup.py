from setuptools import setup, find_packages

#next time:
#python setup.py register
#python setup.py sdist upload

version = open('voicebase/VERSION', 'r').readline().strip()

long_desc = """
Unofficial Python API wrapper for Voicebase API v2
[Documentation](https://voicebase.readthedocs.org/en/latest/)
[Report a Bug](https://github.com/gdoermann/voicebase/issues)
"""

setup(
    name='voicebase',
    version=version,
    description='Unofficial Python API wrapper for Voicebase API v2',
    long_description=long_desc,
    classifiers = [
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='transcription,voicebase,audio',
    install_requires = ['six >= 1.7.2'],
    author='Greg Doermann',
    author_email='dev@doermann.me',
    url='https://github.com/gdoermann/voicebase',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
)