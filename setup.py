from distutils.core import setup

setup(
    name = 'raposa',
    version = '0.1',
    description = 'Lexicological framework for pipeline text processing',
    long_description = """
        RAPOSA processes texts word by word and applies different filters
        in a conveyor-belt like fashion.

        Each filter first adds its own tags to each word according to
        their specific purpose, and then may decide to discard the word
        altogether after evaluating the tags present.

        The words that reach the end of this pipeline are output along
        with their tags and context information. The particular set
        of filters and their order of application is chosen by the user
        from the available pool in each run.

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