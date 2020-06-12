# this file is run using when using "python -m basicmonitor"

import argparse


parser = argparse.ArgumentParser(description='Run baiscmonitor')
parser.add_argument(
	'-prefix',
	type=str,
	help='Prefix to run the webapp and api from. The prefix will be applied to every route.',
	default=None,
)
parser.add_argument(
	'-port', '-p',
	type=str,
	help='Port on which the flask server will listen',
	default=None,
)
parser.add_argument(
	'-host',
	type=str,
	help='Address, the flaks server will listen on',
	default=None,
)
kwargs = {key:value for key, value in parser.parse_args().__dict__.items() if value is not None}


from basicmonitor import run

run(**kwargs)