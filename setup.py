from setuptools import setup, find_packages

import versioneer


setup(
    name="autosubtakeover",
    license='MIT',
    version= '0.1',
    description="autoSubTakeover",
    url="https://github.com/jordyzomer/autosubtakeover",
    download_url = 'https://github.com/jordyzomer/autosubtakeover/archive/v_01.tar.gz',
    author="Jordy Zomer",
    author_email="jordy@simplyhacker.com",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["click", "asyncio", "tornado", "aiodns", "pycares", "tldextract"],
    entry_points={"console_scripts": ["autosubtakeover=autosubtakeover.command:main"]},
)
