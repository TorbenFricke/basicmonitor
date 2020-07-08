from urllib import parse


def apply_validation_mask(data, mask):
	out = {}
	for key, validator in mask.items():
		if not key in data:
			continue
		try:
			if validator is None:
				out[key] = data[key]
			elif isinstance(validator, _ConditionalValidator):
				out.update(validator(key, data))
			else:
				out[key] = validator(data[key])
		except Exception as e:
			raise ValueError(f"Error while validating '{key}': {str(e)}")
	return out


class _ConditionalValidator:
	def __init__(self, condition_validator, validation_masks):
		self.condition_validator = condition_validator
		self.validation_masks = validation_masks

	def __call__(self, condition_key, data):
		# validate condition
		condition = self.condition_validator(data[condition_key])
		# validate the rest
		out = {}
		if condition in self.validation_masks:
			out.update(apply_validation_mask(data, self.validation_masks[condition]))
		out[condition_key] = condition
		return out


def conditional_validator(condition_validator, validation_masks):
	return _ConditionalValidator(condition_validator, validation_masks)


def positive_float(number):
	return abs(float(number))


def url_safe(url):
	return parse.quote(url)


def whitelist(white_list, preprocessor=None):
	def wrapped(value):
		if callable(preprocessor):
			value = preprocessor(value)
		assert value in white_list, "Value not allowed"
		return value
	return wrapped


def boolean(value):
	if value:
		return True
	else:
		return False


def non_empty_string(value):
	s = str(value)
	if s == "":
		raise ValueError("String must not be empty")
	return s


def string(value):
	return str(value)


def is_type(type_str):
	def wrapped(value):
		assert type(value) == type_str, "Type does not match {}".format(type_str)
		return value
	return wrapped


def number_greater_than(threshold):
	def wrapped(number):
		number = float(number)
		assert number > threshold, "Value below threshold of {}".format(threshold)
		return number
	return wrapped


def integer(number):
	return int(number)


def list_validator(validator):
	def wrapped(some_list):
		assert type(some_list) is list, "Not a list"
		return [validator(item) for item in some_list]
	return wrapped