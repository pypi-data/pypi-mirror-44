from setuptools import setup

from runscript import __version__

setup(
    name="script-runner",
    version=__version__,
    license="GPL",
    description="A wrapper for running scripts",
    author="Kang Min Yoo",
    author_email="kaniblurous@gmail.com",
    url="https://github.com/kaniblu/script-runner",
    packages=["runscript"],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Java",
        "Programming Language :: Python",
    ],
    platforms=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "pyyaml"
    ],
    entry_points={
        "console_scripts": ["runscript=runscript.__main__:main"]
    }
)
