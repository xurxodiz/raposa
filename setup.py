from distutils.core import setup

setup(
    name = 'raposa',
    version = '0.2',
    description = 'Lexicological framework for pipeline text processing',
    long_description = """
        RAPOSA processes texts word by word and applies different filters
        in a conveyor-belt like fashion.

        Define a pipeline, with its tokenization method, and the different
        tubes through which the tokens will travel. Tubes may modify
        the token, discard it, tag it, or any combination of those three.
        Some basic pipelines and tubes are included, but every case
        is different, so customization was the key guiding principle.
        As such, we encourage to check the `demo.py` file and the code
        itself to know how to create and combine your own derived classes.

        The intended use case for RAPOSA is lexicology analysis,
        being of special convenience for neology, lexicography
        and morphology, but its open-endedness and customization
        allow for many different kinds of purposes. For this reason,
        it also includes many other NLP/CompLing goodies.

        RAPOSA is not tied to any specific language, though currently
        it may only contain filters for some languages due to
        obvious time development constraints. RAPOSA is specially
        proud to support minorized and minority languages.

        Contributions are always warmly welcome and appreciated!
    """,
    author='Xurxo Diz Pico',
    author_email='xurxo@xurxodiz.eu',
    url='http://github.com/xurxodiz/raposa',
    classifiers=[
        "Development Status :: 3 - Alpha", \
        "Environment :: Console", \
        "Intended Audience :: Science/Research", \
        "License :: OSI Approved :: MIT License", \
        "Natural Language :: Galician", \
        "Operating System :: OS Independent", \
        "Programming Language :: Python", \
        "Programming Language :: Python :: 3", \
        "Topic :: Text Processing :: Filters", \
        "Topic :: Text Processing :: Linguistic" \
    ],
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'nltk',
        'emoji',
        'exrex'
    ],
    packages=find_packages(exclude=[]), # add if necessary
)