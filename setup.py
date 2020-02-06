# vi: set ft=python sts=4 ts=4 sw=4 et:


from setuptools import setup

setup(
    name='smartydoc',
    version='0.0.2',
    description='Utilities for converting notebook into customized html',
    author='Lijie Huang',
    author_email='huanglijie@outlook.com',
    packages=['smartydoc'],
    scripts=['bin/trans2std']
    package_data={'smarty': ['template/*']},
    install_requires=[
        'plotly'
    ],
    download_url = 'https://github.com/sealhuang/SmartyDoc/archive/master.zip'
)
