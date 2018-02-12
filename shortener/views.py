from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import CirrURL
from .forms import SubmitUrlForm
from .utils import correctURL

from analytics.models import ClickEvent

class HomeCBView(View):
	def get(self, request, *args, **kwargs):
		form = SubmitUrlForm()
		context = {
			'title': 'Cirr.com',
			'form': form
		}
		return render(request, 'shortener/home.html', context)
	def post(self, request, *args, **kwargs):
		# print(request.POST)
		# print(request.POST.get('url'))

		form = SubmitUrlForm(request.POST)
		context = {
			'title': 'Cirr.com',
			'form': form
		}
		template = 'shortener/home.html'

		if form.is_valid():
			''' Add http:// to url'''
			url = correctURL(form.cleaned_data.get('url'))
			obj, created = CirrURL.objects.get_or_create(url=url)
			context = {
				'object': obj,
				'created': created
			}
			if created:
				template = 'shortener/success.html'
			else:
				template = 'shortener/already-exists.html'

		return render(request, template, context)

# def cirr_redirect_view(request, shortcode = None, *args, **kwargs):
# 	# ''' Handle page not found by exception '''
# 	# obj = CirrURL.objects.get(shortcode=shortcode)
# 	# try:
# 	# 	obj = CirrURL.objects.get(shortcode=shortcode)
# 	# except:
# 	# 	obj = CirrURL.objects.all().first()
	
# 	# ''' Handle page not found by query set '''
# 	# obj_url = None
# 	# qs = CirrURL.objects.filter(shortcode__iexact=shortcode)
# 	# if qs.exists() and qs.count() == 1:
# 	# 	obj = qs.first()
# 	# 	obj_url = obj.url
# 	print('shortcode: %s'%shortcode)
# 	obj = get_object_or_404(CirrURL, shortcode=shortcode)

# 	# return HttpResponse('hello {url}'.format(url=obj.url))
# 	return HttpResponseRedirect(obj.url)

class URLRedirectCBView(View):
	def get(self, request, shortcode = None, *args, **kwargs):
		print('shortcode: %s'%shortcode)
		obj = get_object_or_404(CirrURL, shortcode=shortcode)

		print(obj)
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)

		# ''' Option2 '''
		# qs = CirrURL.objects.filter(shortcode__iexact=shortcode)
		# if qs.count != 1 and not qs.exists():
		# 	raise Http404
		# obj = qs.first()
		# print(ClickEvent.objects.create_event(obj))
		# return HttpResponseRedirect(obj.url)

	def post(self, request, *args, **kwargs):
		return HttpResponse()