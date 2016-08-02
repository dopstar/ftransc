from setuptools import setup

requirements = [
    'requests',
    'mutagen',
    'blessings',
]

setup_args = {
    'name': 'ftransc',
    'version': '6.0.1',
    'author': 'Mkhanyisi Madlavana',
    'author_email': 'mkhanyisi@gmail.com',
    'url': 'https://github.com/dopstar/ftransc',
    'download_url': 'https://github.com/dopstar/ftransc/tarball/6.0.0',
    'package_dir': {'ftransc': 'ftransc'},
    'description': 'ftransc is a python library for converting audio files across various formats.',
    'long_description': 'ftransc is a python library for converting audio files across various formats.',
    'packages': [
        'ftransc',
        'ftransc.core',
        'ftransc.config',
        'ftransc.metadata',
        'ftransc.core.queue',
    ],
    'package_data': {'ftransc': ['*.md', 'config/data/*.json']},
    'install_requires': requirements,
    'keywords': 'Audio, Convert, ffmpeg, avconv, mp3',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    'entry_points': {
        'console_scripts': [
            'ftransc=ftransc.launcher:cli',
        ]
    }
}

setup(**setup_args)
