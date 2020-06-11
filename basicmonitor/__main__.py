# this file is run using when using "python -m basicmonitor"

import argparse


parser = argparse.ArgumentParser(description='Run baiscmonitor')
parser.add_argument(
	'-prefix',
	type=str,
	help='Prefix to run the webapp and api from. The prefix will be applied to every route.',
	default="",
)
parser.add_argument(
	'-port', '-p',
	type=str,
	help='Port on which the flask server will listen',
	default=5000,
)
args = parser.parse_args()


from basicmonitor import run

run(prefix=args.prefix, port=args.port)