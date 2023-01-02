from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in alfouz_mod/__init__.py
from alfouz_mod import __version__ as version

setup(
	name="alfouz_mod",
	version=version,
	description="Alfouz Customization",
	author="ARD",
	author_email="ard.ly",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
