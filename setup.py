from setuptools import setup, find_packages

requirements = [
	"psutil",
	"flask",
	"flask-restful",
	"Flask-Compress",
	"simpleeval",
]

setup(
	name='basicmonitor',
	version='0.1.3dev8',
	description='A Super Simple Monitoring Webapp Thingi',
	author='Torben Fricke',
	url='https://www.python.org/sigs/distutils-sig/',
	packages=find_packages(),
	package_data={'basicmonitor': [
		'build/*',
		'static/*',
		'templates/*',
	]},
)