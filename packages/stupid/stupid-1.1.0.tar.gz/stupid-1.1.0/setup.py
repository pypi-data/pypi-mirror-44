import setuptools # noqa Needed for bdist_wheel
from distutils.core import setup

setup(
    name='stupid',
    version='1.1.0',
    author='masell',
    url='https://github.com/masell/stupid',
    packages=['stupid'],
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: BSD License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    license='BSD',
    install_requires=['dataclasses'],
    description="Support for multiple inheritance and __slots__",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
