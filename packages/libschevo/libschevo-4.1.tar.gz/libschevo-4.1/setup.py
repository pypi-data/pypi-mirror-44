#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
sys.path.append('lib')
PY3K = sys.version_info[0] == 3

from textwrap import dedent
from setuptools import setup, Extension, find_packages
from schevo.release import VERSION

# basic requirements
basic_requires = [
        'bcrypt >= 3.1.6',
        'transaction >= 2.4.0'
        ]

# python 2.7 requirements
schevo_requires = [
        'libdurus >= 4.0',
        'trollius >= 2.2'
       ]

if not PY3K:
    install_requires = basic_requires + schevo_requires
else:
    install_requires = basic_requires

setup(
    name='libschevo',
    version=VERSION,
    description='Next-generation Object-Oriented DBMS',
    long_description=dedent("""
    Schevo is a next-generation DBMS that focuses on the following:

    * **Rapid Development**.

      It's easy and fun to create even the most complex of
      databases. Easily write and understand schema syntax. Quickly
      place required initial data directly in your schema; use the
      same syntax to create sets of sample data for development use.

    * **Rich Schema Definition**.

      Write database schemata using concise, easy-to-read Python
      code. Your schema will describe not only database structure, but
      also all transactions and rules that ensure database integrity.

    * **Automated Schema Evolution**.

      Deploy a Schevo database and use it to store valuable data, then
      easily make further changes to the structure of the
      database. Use Schevo's tools to help restructure a database and
      safely migrate data from one schema version to the next.

    * **Transaction Based**.

      Schevo protects your data. Use transactions to make all changes
      to a Schevo database (it's the only way it allows you to!), and
      you can trust Schevo to ensure that your database is left in a
      consistent state at all times.

    * **User Interface Generation**.

      User interface code takes advantage of the richness of your
      database schema. Use a full-featured database navigator to
      interact with your database without writing a single line of
      code outside your database schema. Build customized UIs using
      Schevo-aware widgets and UI tools.

    """),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Database :: Database Engines/Servers',
            'Topic :: Software Development :: Libraries :: '
                'Application Frameworks',
        ],
        keywords='database dbms schevo libschevo',
        maintainer='Etienne Robillard',
        maintainer_email='admin@isotopesoftware.ca',
        url='https://www.isotopesoftware.ca/software/libschevo/',
        license='Apache 2.0 License',
        packages=find_packages(where='lib', exclude=['doc', 'test']),
        package_dir={
            '': 'lib',
        },
        #include_package_data=True,
        #package_data={
        #    'schevo.test.icons': ['*.png'],
        #},
        scripts=[
            'tools/schevo-daemonize',
            'tools/schevo-editor',
            'tools/schevo-initdb',
            'tools/schevo-export',
            'tools/schevo-upgradedb'
            ],
        zip_safe=False,
        install_requires=install_requires,
        #tests_require=['nose >= 0.10.4'],
        #test_suite='nose.collector',
        ext_modules=[
            Extension('schevo.store._s_persistent', 
                ['lib/schevo/store/_s_persistent.c']),
        ],
        entry_points = """
        [console_scripts]
        schevo = schevo.script.main:start
        schevo_hotshot = schevo.script.main:start_hotshot

        [schevo.backend]
        zodb = schevo.backends.zodb:ZodbBackend
        durus = schevo.backends.durus39:DurusBackend


        [schevo.schevo_command]
        backends = schevo.script.backends:start
        db = schevo.script.db:start
        shell = schevo.script.shell:start
        editor = schevo.gtk2.script:start
        """,
        )

