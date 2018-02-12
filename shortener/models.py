from django.db import models
from django.conf import settings
# from django.urls import reverse
from django_hosts.resolvers import reverse
from .utils import code_generator, create_shortcode
from .validators import validate_url, validate_dot_com
# Create your models here.

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class CirrURLManager(models.Manager):
	def all(self, *args, **kwargs):
		qs_main = super(CirrURLManager, self).all(*args, **kwargs)
		qs = qs_main.filter(active=True)
		return qs_main

	def refresh_shortcode(self, items=None):
		qs = CirrURL.objects.filter(id__gte=1)
		print('items: %s'%items)
		if items is not None and isinstance(items, int):
			qs = qs.order_by('id')[:items]
		new_codes_num = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			print(q.id)
			print(q.shortcode)
			new_codes_num += 1
		print('New codes: {i}'.format(i=new_codes_num))

class CirrURL(models.Model):
	url = models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
	shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = CirrURLManager()

	def save(self, *args, **kwargs):
		print("save")
		if self.shortcode is None or self.shortcode == "":
			self.shortcode = create_shortcode(self)

		super(CirrURL, self).save(*args, **kwargs)


	# def mysave(self):
	# 	self.save()

	def __str__(self):
		return str(self.url)

	def __unicode__(self):
		return str(self.url)

	def get_short_url(self):
		# ''' Hardcode '''
		# return 'http://www.tirr.com/{shortcode}'.format(shortcode=self.shortcode)

		# ''' Dynamic way '''
		port = str(settings.DEFAULT_PORT) if (settings.DEFAULT_PORT is not None and settings.DEFAULT_PORT != 80) else None

		url_path = reverse('scode',kwargs={'shortcode':self.shortcode}, host='www', scheme='http', port=port)
		return url_path
		