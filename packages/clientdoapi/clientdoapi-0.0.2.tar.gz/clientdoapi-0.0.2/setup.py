import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clientdoapi",
    version="0.0.2",
    author="Max J. Rodriguez Beltran",
    author_email="maxjrb@openitsinaloa.com",
    description="A module to manage Digital Ocean API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jaxmetalmax/clientdoapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    install_requires=['requests'],

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/Jaxmetalmax/clientdoapi/issues',
        'Say Thanks!': 'https://www.openitsinaloa.com',
        'Source': 'https://github.com/Jaxmetalmax/clientdoapi',
    },
)
