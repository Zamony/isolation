import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="isolation",
    version="1.0.0",
    description="isolation is a two-player strategy board game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zamony/isolation",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'isolation = isolation.cli:main',
        ],
    },
    install_requires=[
          'pygame==2.0.0.dev8',
          'pygame_menu==3.0.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)