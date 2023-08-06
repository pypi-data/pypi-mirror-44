from setuptools import setup
from setuptools import find_packages


def readme():
    with open("README.md") as f:
        return f.read()


def required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="zradio",
    version="0.0.dev1",  # versionamento https://www.python.org/dev/peps/pep-0440/
    description="terminal radio.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="radio browser web terminal command line",
    author="André P. Santos",
    author_email="andreztz@gmail.com",
    url="https://github.com/andreztz/zradio",
    license="MIT",
    packages=find_packages(),
    install_requires=required(),
    entry_points={"console_scripts": ["zradio=radio.app:main"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python :: 3.7",
    ],
)
