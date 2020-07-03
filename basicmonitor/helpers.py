#import hashlib, random, base64
#_seed = bytes(str(random.random()), encoding="utf8")
#_idx = 0
#def uid():
#	global _idx
#	_idx += 1
#
#	sha = hashlib.sha3_256()
#	sha.update(_seed)
#	sha.update(bytes(str(_idx), encoding="utf8"))
#	return str(base64.b64encode(sha.digest()), "utf8")

import uuid

def uid():
	return str(uuid.uuid4())


def do_nothing(*args, **kwargs):
	pass