import os
import setuptools

short_description = 'A composite based data manager'
if os.path.exists('README.md'):
    with open('README.md', 'r') as fh:
        long_description = fh.read()

else:
    long_description = short_description

setuptools.setup(
    name='fracture',
    version='0.0.1',
    author='Mike Malinowski',
    author_email='mike@twisted.space',
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikemalinowski/fracture',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)