from urllib import parse


def apply_validation_mask(data, mask):
	out = {}
	for key, validator in mask.items():
		if not key in data:
			continue
		try:
			if validator is None:
				out[key] = data[key]
			else:
				out[key] = validator(data[key])
		except Exception as e:
			raise ValueError(f"Error while validating '{key}':\n{e}")
	return out


def positive_float(number):
		return abs(float(number))


def url_safe(url):
	return parse.quote(url)


def whitelist(white_list):
	def wrapped(value):
		assert value in white_list
		return value
	return wrapped


def boolean(value):
	if value:
		return True
	else:
		return False


def is_type(type_str):
	def wrapped(value):
		assert type(value) == type_str
		return value
	return wrapped