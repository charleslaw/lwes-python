# -*- coding: utf-8 -*-

from setuptools import setup

long_desc = '''
The LWES python client is a pure Python implementation of the LWES client.
'''

setup(
    name='lwes',
    version='0.0.1',
    url='http://github.com/charleslaw/lwes-python',
    license='BSD',
    author='Charles Law',
    author_email='charles.law@openx.com',
    description='Pure Python LWES Client',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=['lwes'],
    include_package_data=False,
    install_requires=[],
    namespace_packages=['lwes']
)
