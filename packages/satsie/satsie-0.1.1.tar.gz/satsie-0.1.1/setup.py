# -*- coding: utf-8 -*-

import setuptools


# with open('README.md', 'r') as readme_file:
#     long_description = readme_file.read()


with open('requirements.txt', 'r') as requirements_file:
    requirements = requirements_file.read()


setuptools.setup(
    name='satsie',
    version='0.1.1',
    author='vjyq',
    author_email='yuqing.ji@outlook.com',
    description='a tool to check for your subscription updates.',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://github.com/vjyq/satsie.git',
    install_requires=requirements,
    packages=setuptools.find_packages(include=[
        'satsie',
        'satsie.subscription',
        'satsie.utils',
        'satsie.settings',
    ]),   
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    test_suite='./satsie/tests',
)
