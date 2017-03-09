from django.shortcuts import render

# Create your views here.
#	for api purpose
import json

# 	Important code

# 
# 	To 
from django.contrib.auth.decorators import login_required
# 
# 	paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden)
#
#	getting object out of the database
from django.shortcuts import get_object_or_404

# for forms
from django.template.context_processors import csrf
from django.contrib.loader import render_to_string


FEEDS_NUM_PAGES = 10


@login_required
def feeds(request):
	all_feeds = Feed.get_feeds()
	paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
	feeds = paginator.page(1)
	from_feed = -1

	if feeds:
		from_feed = feeds[0].id

	context = {
		'feeds': feeds, 
		'from_feed' : from_feed,
		'page' : 1,
	}

	return render(request, 'feeds/feeds.html', context )

# individual feed
def feed(request, pk):
	feed = get_object_or_404(Feed, pk=pk)

	context = {
		'feed': feed,
	}
	return render(request, 'feeds/feed.html', context)


@login_required
@ajax_required
def load(request):
	# defines the parameters 
	from_feed = request.GET.get('from_feed')
	page = request.GET.get('page')
	feed_source = request.GET.get('feed_source')
	
	# all feels come through it
	all_feeds = Feed.get_feeds(from_feed)

	if feed_source != 'all':
		all_feeds = all_feeds.filter(user_id=feed_source)

	paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)

	try:
		feeds = paginator.page(page)
	# why?
	except PageNotAnInteger:
		return HttpResponseBadRequest()
	except EmptyPage:
		feeds = []

	#  why?
	html = ''

	# why? we can directly add it to the html form
	#
	csrf_token = (csrf(request)['csrf_token'])

	for feed in feeds:
		html = '{0}{1}'.format(html, 
				render_to_string())

		# render_to_string(template_name, context=None, request=None, using=None)[source]¶
		# render_to_string() loads a template like get_template() 
		# and calls its render() method immediately. 
		
