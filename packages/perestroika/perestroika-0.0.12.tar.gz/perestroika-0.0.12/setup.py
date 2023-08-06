from setuptools import setup, find_packages

version = "0.0.12"

setup(
    name="perestroika",
    packages=find_packages(),
    version=version,
    description="Rest lib",
    long_description="Rest lib",
    author="Ruslan Roskoshnyj",
    author_email="i.am.yarger@gmail.com",
    url="https://github.com/newmediatech/perestroika",
    download_url="https://github.com/newmediatech/perestroika/archive/{}.tar.gz".format(version),
    keywords=["REST"],
    classifiers=[],
    python_requires=">3.6.0",
    platforms=["OS Independent"],
    license="LICENSE.txt",
    install_requires=[
        "validate-it (==0.4.1)",
        "attrs (==19.1.0)",
    ],
    extras_require={
        "tests": [
            "pytest (==3.6.0)",
            "coverage (==4.5)",
            "pytest-cov (==2.5.1)",
            "django (==2.1.4)",
            "pytest-django (==3.2.0)",
        ],
        "docs": []
    }
)
