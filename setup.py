"""Set up files
"""

import setuptools

setuptools.setup(name="fpipy",
	version = "0.0.0",
	description = "Tools for analysing FPI data",
	author = "Elliott Day",
	url = "https://github.com/ellioday/FPIpy",
	packages = setuptools.find_packages(exclude=["test"]),
	classifiers = ["Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	],
	python_requires=">=3.6",
	install_requires=["numpy", "h5py", "pydatadarn"],
)
