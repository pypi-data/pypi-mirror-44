from setuptools import setup, find_packages

from pyms import name, __version__, __maintainer_email__, __url__

setup(
	name=name,
	version=__version__,
    author='Dominic Davis-Foster',
	author_email=__maintainer_email__,
	packages=find_packages(),
	license="GNU General Public License v2.0",
	url=__url__,
	description='Python Toolkit for Mass Spectrometry',
	long_description="""PyMassSpec is a collection of PyMS libraries which can be used to perform peak picking,
alignment by dynamic programming, and gap-filling in Gas Chromatography Mass Spectrometry experiments.""",
	install_requires=[
	        "numpy >= 1.16.2",
	        "scipy >= 1.2.1",
	        "pymzml >= 2.2.1",
			"matplotlib >= 3.0.2",
        	],
)

# Original Author Sean O'Callaghan <spoc@unimelb.edu.au>,