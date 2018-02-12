from django.conf import settings
import random
import string

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 4)

def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase+string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

''' Generate shortcode that is not repeated with an existsing one
'''
def create_shortcode(instance, size=SHORTCODE_MIN):
	new_code = code_generator(size=size)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(shortcode=new_code).exists()
	if qs_exists:
		return code_generator(size=size)
	return new_code

def correctURL(url):
	if not url.startswith('http://'):
		url = 'http://'+url
	return url