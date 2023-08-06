import os

from setuptools import find_packages, setup

version = '0.0.1'

setup(
    name='polecat',
    version=version,
    author='Luke Hodkinson',
    author_email='furious.luke@gmail.com',
    maintainer='Luke Hodkinson',
    maintainer_email='furious.luke@gmail.com',
    description='',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.md')
    ).read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License'
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.js', '*.html', '*.*']},
    install_requires=[
        'psycopg2-binary',
        'graphql-core-next',
        'pytest',
        'factory_boy',
        'click',
        'sanic'
    ],
    dependency_links=[],
    entry_points={
        'console_scripts': [
            'polecat=polecat.cli.entrypoint:entrypoint'
        ]
    },
    zip_safe=False
)
