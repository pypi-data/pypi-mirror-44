from setuptools import setup
import sys
if sys.version_info < (3,3):
    sys.exit('Pirogue requires at least Python version 3.3.\nYou are currently running this installation with\n\n{}'.format(sys.version))

setup(
    name = 'pirogue',
    packages = [
        'pirogue'
    ],
    scripts = [
        'scripts/pirogue'
    ],
    version = '0.1',
    description = 'PostgreSQL view generator',
    author = 'Denis Rouzaud',
    author_email = 'denis.rouzaud@gmail.com',
    url = 'https://github.com/opengisch/pirogue',
    download_url = 'https://github.com/opengisch/pirogue/archive/0.1.tar.gz', # I'll explain this in a second
    keywords = [
        'postgres'
    ],
    classifiers = [
        'Topic :: Database',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Development Status :: 3 - Alpha'
    ],
    install_requires = [
        'psycopg2-binary>=2.7.3'
    ],
    python_requires=">=3.3",
)
