from django.db import models
from shortener.models import CirrURL

class ClickEventManage(models.Manager):
	def create_event(self, instance):
		if isinstance(instance, CirrURL):
			obj, created = self.get_or_create(cirr_url=instance)
			obj.count += 1
			obj.save()
			return self.count
		return None

class ClickEvent(models.Model):
	cirr_url = models.OneToOneField(CirrURL, on_delete=models.CASCADE)
	count = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = ClickEventManage()

	def __str__(self):
		return '{i}'.format(i=self.count)
