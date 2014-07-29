from setuptools import setup

setup(
    name='phrase_recognizer',
    version='0.0.1',
    url='http://github.com/17zuoye/phrase_recognizer/',
    license='MIT',
    author='David Chen',
    author_email=''.join(reversed("moc.liamg@emojvm")),
    description='Phrase Recognizer',
    long_description='Phrase Recognizer',
    packages=['phrase_recognizer',],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'split_block',
        'etl_utils',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
