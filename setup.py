from setuptools import setup

requirements = [
    'requests',
    'mutagen',
    'blessings',
]

setup_args = {
    'name': 'ftransc',
    'version': '6.0.0',
    'author': 'Mkhanyisi Madlavana',
    'author_email': 'mkhanyisi@gmail.com',
    'url': 'http://github.com/dopstar/ftransc',
    'package_dir': {'ftransc': 'ftransc'},
    'description': 'ftransc is a python library for converting audio files across various formats.',
    'long_description': 'ftransc is a python library for converting audio files across various formats.',
    'packages': [
        'ftransc',
    ],
    'package_data': {'ftransc': ['*.md', 'config/data/*.json']},
    'install_requires': requirements,
    'keywords': 'Audio, Convert, FFMpeg',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    'entry_points': {
        'console_scripts': [
            'ftransc=ftransc.launcher:cli',
            'ftransc_qt=ftransc.launcher:gui',
        ]
    }
}

setup(**setup_args)
