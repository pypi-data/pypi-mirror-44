import setuptools

version = '0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbcw",
    version=version,
    author="stefanitsky",
    author_email="stefanitsky.mozdor@google.com",
    description="Database connection wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Stefanitsky/dbcw",
    packages=setuptools.find_packages(),
    scripts=['dbcw/dbcw.py'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Database :: Front-Ends'
    ],
)