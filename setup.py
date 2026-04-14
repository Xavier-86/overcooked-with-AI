from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="overcooked-with-AI",
    version="0.2.0",
    author="ZSC-Eval Team",
    author_email="",
    description="Overcooked Human-AI Testing Tool with Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ZSC-Eval",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "overcooked-human-test=human_test.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
