#!/usr/bin/env python

import os

from setuptools import setup, find_packages

module_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    setup(
        name="maggma",
        version="0.13.0",
        description="MongoDB aggregation machine",
        long_description=open(os.path.join(module_dir, "README.md")).read(),
        url="https://github.com/materialsproject/maggma",
        author="MP Team",
        author_email="matproj-develop@googlegroups.com",
        license="modified BSD",
        packages=find_packages(),
        package_data={},
        zip_safe=False,
        install_requires=[
            "pymongo>=3.6", "mongomock>=3.10.0", "monty>=1.0.2",
            "smoqe>=0.1.3", "PyYAML>=3.12", "pydash>=4.1.0", "tqdm>=4.19.6",
            "mongogrant>=0.2.2", "hvac>=0.3.0", "boto3>=1.6.9",
        ],
        extras_require={"mpi": ["mpi4py>=2.0.0"]},
        classifiers=["Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.6",
                     "Development Status :: 2 - Pre-Alpha",
                     "Intended Audience :: Science/Research",
                     "Intended Audience :: System Administrators",
                     "Intended Audience :: Information Technology",
                     "Operating System :: OS Independent",
                     "Topic :: Other/Nonlisted Topic",
                     "Topic :: Database :: Front-Ends",
                     "Topic :: Scientific/Engineering"],


        entry_points={
            "console_scripts": [
                "mrun = maggma.cli.mrun:main"
                ]
            },
        test_suite="nose.collector",
        tests_require=["nose"],
        python_requires='>=3.6',
    )
