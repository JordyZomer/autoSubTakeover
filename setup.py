from setuptools import setup, find_packages

import versioneer


setup(
    name="autosubtakeover",
    license='MIT',
    version= '0.1',
    cmdclass=versioneer.get_cmdclass(),  # type: ignore
    description="autoSubTakeover",
    url="https://github.com/jordyzomer/autosubtakeover",
    download_url = 'https://github.com/jordyzomer/autosubtakeover/archive/v_01.tar.gz',
    author="Jordy Zomer",
    author_email="jordy@simplyhacker.com",
    packages=find_packages(),
    install_requires=["click", "asyncio", "tornado", "aiodns", "pycares", "tldextract"],
    entry_points={"console_scripts": ["autosubtakeover=autosubtakeover.command:main"]},
)
