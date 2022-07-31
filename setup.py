from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='rotation-helper',
    version='0.1.0',
    description='XIV Helper',
    author='Ryan Westwood',
    author_email='ryanwestwood7@outlook.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "async-generator==1.10",
        "attrs==21.4.0",
        "blinker==1.5",
        "Brotli==1.0.9",
        "certifi==2022.6.15",
        "cffi==1.15.1",
        "charset-normalizer==2.1.0",
        "cryptography==37.0.4",
        "h11==0.13.0",
        "h2==4.1.0",
        "hpack==4.0.0",
        "hyperframe==6.0.1",
        "idna==3.3",
        "kaitaistruct==0.10",
        "outcome==1.2.0",
        "pyasn1==0.4.8",
        "pycparser==2.21",
        "pydivert==2.1.0",
        "pyOpenSSL==22.0.0",
        "pyparsing==3.0.9",
        "PySDL2==0.9.12",
        "pysdl2-dll==2.0.22.post1",
        "PySocks==1.7.1",
        "python-dotenv==0.20.0",
        "requests==2.28.1",
        "selenium==4.3.0",
        "selenium-wire==4.6.5",
        "sniffio==1.2.0",
        "sortedcontainers==2.4.0",
        "trio==0.21.0",
        "trio-websocket==0.9.2",
        "urllib3==1.26.10",
        "webdriver-manager==3.8.2",
        "wsproto==1.1.0",
        "zstandard==0.18.0"
    ],
    extras_require = {
        "dev": [
            "pylint==2.14.5",
            "autopep8==1.6.0"
        ]
    }
)
