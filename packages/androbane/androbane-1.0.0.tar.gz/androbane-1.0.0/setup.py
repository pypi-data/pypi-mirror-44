import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

req=["requests","PySocks","bs4","mysql-connector","scapy","stem"]

setuptools.setup(
    name="androbane",
    version="1.0.0",
    author="AlaBouali",
    author_email="trap.leader.123@gmail.com",
    description="cyber security library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlaBouali/andorbane",
    python_requires=">=2.7",
    install_requires=req,
    packages=["androbane"],
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: Unix",
    ],
)
