from setuptools import setup

version = '6.0.5'

requirements = [
    'nose',
    'pafy',
    'mutagen',
    'plumbum',
    'blessings',
    'youtube-dl',
]


if 'a' in version:
    dev_status = '3 - Alpha'
elif 'b' in version:
    dev_status = '4 - Beta'
else:
    dev_status = '5 - Production/Stable'

setup_args = {
    'name': 'ftransc',
    'version': version,
    'author': 'Mkhanyisi Madlavana',
    'author_email': 'mkhanyisi@gmail.com',
    'url': 'https://github.com/dopstar/ftransc',
    'download_url': 'https://github.com/dopstar/ftransc/tarball/{0}'.format(version),
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
        'Development Status :: {0}'.format(dev_status),
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    'entry_points': {
        'console_scripts': [
            'ftransc=ftransc.launcher:cli',
        ]
    }
}

setup(**setup_args)
