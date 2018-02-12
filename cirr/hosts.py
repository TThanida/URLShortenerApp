from django.conf import settings
from django_hosts import patterns, host
from cirr.hostsconf import urls as redirect_urls

host_patterns = patterns('',
	## Point both www and non-www to ROOT_URLCONF
	host(r'.*', settings.ROOT_URLCONF, name='www')

    # host(r'www', settings.ROOT_URLCONF, name='www'),
    # host(r'(?!www).*', redirect_urls, name='wildcard')
)