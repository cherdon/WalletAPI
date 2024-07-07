import setuptools

with open("README.md", "r") as file:
    long_description = file.read()


setuptools.setup(
    name='walletapi',
    version='1.0.0',
    author='Liew Cher Don',
    author_email='liewcherdon@gmail.com',
    description='Simple Python Wrapper for scraping and accessing Wallet App by Budgetbakers Data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cherdon/WalletAPI',
    packages=['walletapi'],
    classifiers=[
     "Programming Language :: Python :: 3.9",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ]
)