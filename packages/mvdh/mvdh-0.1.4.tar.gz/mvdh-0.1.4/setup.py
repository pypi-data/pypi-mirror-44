import setuptools

with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name         = 'mvdh',
    version      = '0.1.4',
    author       = 'Matthew P. Humphreys',
    author_email = 'm.p.humphreys@cantab.net',
    description  = 'Miscellaneous Python tools',
    url          = 'https://github.com/mvdh7/mvdh',
    packages     = setuptools.find_packages(),
    install_requires = ['autograd==1.2'],
    dependency_links = ['https://github.com/mvdh7/autograd/tarball/master'],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = (
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',),)
