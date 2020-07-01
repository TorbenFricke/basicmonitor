from setuptools import setup, find_packages

requirements = [
	"psutil",
	"flask",
	"flask-restful",
	"flask-compress",
	"simpleeval",
]

import os

def package_files(directory):
	# source: https://stackoverflow.com/questions/27664504/how-to-add-package-data-recursively-in-python-setup-py
	paths = []
	for (path, directories, filenames) in os.walk(directory):
		for filename in filenames:
			paths.append(os.path.join('..', path, filename))
	return paths

build_files = package_files('basicmonitor/build')

setup(
	name='basicmonitor',
	version='0.2.1',
	description='A Super Simple Monitoring Webapp Thingi',
	author='Torben Fricke',
	url='https://www.python.org/sigs/distutils-sig/',
	packages=find_packages(),
	package_data={'': build_files},
)