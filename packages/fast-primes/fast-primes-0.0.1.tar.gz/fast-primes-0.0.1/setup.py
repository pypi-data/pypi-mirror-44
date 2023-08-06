from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'fast-primes',
    version = '0.0.1',
    description = 'Calculate prime numbers with Cython',
    url = 'https://github.com/Bestoa/PyPrime',
    author = 'Besto',
    author_email = 'bestoapache@gmail.com',
    license = 'AGPL',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    keywords='prime',
    install_requires = ['cython'],
    ext_modules = cythonize(["prime.pyx"], annotate=True)
)
