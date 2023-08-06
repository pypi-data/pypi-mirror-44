import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quantum-dice",
    version="0.3.1",
    author="Justin Peter",
    author_email="planetzzyx@protonmail.com",
    description="A dice using quantum mechanics.",
    long_description="The Quantum Dice leverages the IBM Q quantum computer to generate a truly random set of numbers.",
    long_description_content_type="text/markdown",
    url="https://github.com/TheMagicNacho/quantum-dice",
    packages=setuptools.find_packages(),
    install_requires = ['qiskit'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
