import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "coffeewhale",
    version = "0.0.9",
    author = "Hongkun Yoo",
    author_email = "hongkunyoo@gmail.com",
    description = "coffeewhale, a whale that tells you the job is done, when it's done!",
    license = "MIT License",
    keywords = "slack api, slack notification",
    url = "https://github.com/hongkunyoo/coffeewhale",
    #packages=['azure'],
    packages=find_packages(),
    install_requires=['pytz'],
    long_description="coffeewhale, a whale that tells you the job is done, when it's done!"
)
