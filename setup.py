from distutils.core import setup

requirements = [
	"psutil",
	"flask",
	"flask-restful",
	"Flask-Compress",
	"simpleeval",
]

setup(
	name='Distutils',
	version='0.1',
	description='A Super Simple Monitoring Webapp',
	author='Torben Fricke',
	url='https://www.python.org/sigs/distutils-sig/',
	packages=['basicmonitor'],
)