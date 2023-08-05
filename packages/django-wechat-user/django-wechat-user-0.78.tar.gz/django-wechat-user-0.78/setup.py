import os 
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wechat-user',
    version='0.78',
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    license='BSD License',  # example license
    description='A wechat user model',
    long_description=README,
    url='',
    author='Ken Zhang',
    author_email='kennir@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',  # replace "X.Y" as appropriatetwine upload dist/* -r pypi
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)