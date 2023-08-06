import pathlib

from setuptools import setup

REPO = pathlib.Path(__file__).parent

setup(
    name='linode-dynamic-dns',
    version='0.5.0',
    description='Dynamically set the IP of Linode DNS records ',
    long_description=REPO.joinpath('README.rst').read_text(),
    author='Andrew Rabert',
    author_email='ar@nullsum.net',
    url='https://github.com/nvllsvm/linode-dynamic-dns',
    packages=['linode_dynamic_dns'],
    install_requires=['requests'],
    entry_points={
        'console_scripts': ['linode-dynamic-dns=linode_dynamic_dns:main']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.6'
)
