from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AT_YOUR_SERVICE",
    version="0.1",
    author="Swarnendu",
    packages=find_packages(),
    install_requires = requirements,
)