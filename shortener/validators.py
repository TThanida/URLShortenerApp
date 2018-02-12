from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
	url_validator = URLValidator()
	
	value_http = value
	if not value_http.startswith('http://'):
		value_http = 'http://'+value_http
	try:
		url_validator(value_http)
	except:
		raise ValidationError('Invalid URL for this field')

	return value

def validate_dot_com(value):
	if 'com' not in value:
		raise ValidationError('This is not valid url because no .com')
	return value