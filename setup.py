from setuptools import setup, find_packages

setup(
    name="sudoku",
    version="1.0.0",
    packages=[ 'renlabs.sudoku' ],
    author="Steve Work",
    author_email="steve@work.renlabs.com",
    description="Solve sudoku puzzles",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    zip_safe=True,
    entry_points = {
        "console_scripts": [
            "sudoku = renlabs.sudoku.cli:main"
        ]
    }
)
