from __future__ import unicode_literals

from django.db import models

# Create your models here.
#
#importing the django-user model
from django.contrib.auth.models import User

#
# For compatiblity between python 2 and python 3
from django.utils.encoding import python_2_unicode_compatible

#
# why?
from django.utils.html import escape

#
# 	why?
#	what
from django.utils.translation import ugettext_lazy as _

#  a package?
import bleach



@python_2_unicode_compatible
#
#	Defines only the feed object. The content would be populated 
#	from somewhere else
class Feed(models.Model):
	user = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	post = models.TextField(max_length=250)

	# 
	#   assigns the parent as Feed.
	#	why?
	parent = models.ForeignKey('Feed', null=True, blank=True)
	
	#
	# These must come from the notification app
	likes = models.IntegerField(default=0)
	comments = models.IntegerField(default=0)

	class Meta:
		#
		# Just for the admin panel
		verbose_name = _('Feed')
		verbose_name_plural = _('Feeds')
		ordering = ('-date')


	def __str__(self):
		return self.post


	@staticmethod 
	#	it gets the parameter as from_feed=None
	def get_feeds(from_feed=None):
		if from_feed is not None:
			feeds = Feed.objects.filter(parent=None, id__lte=from_feed)
		else:
			feeds = Feed.objects.filter(parent=None)

		
		return feeds

	@staticmethod
	def get_feeds_after(feed):
		feeds = Feed.objects.filter(parent=None, id__gt=None)
		return feeds

	def get_comments(self):
		return Feed.objects.filter(parent=self).order_by('date')

# This won't work unless we make an app Activity

	# def calculate_likes(self):
	# 	#	calculates every activity object that appears 
	# 	likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk).count()

	# 	self.likes = likes
	# 	self.save()

	# 	return self.likes

	# def get_likes(self):
	# 	likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk)

	# 	return likes 


	# def get_likers(self):
	# 	likes = self.get_likes()
	# 	likers = []

	# 	for like in likes:
	# 		likes.append(like.user)

	# 		return likers


	#	
	# This is calculating the individual comments of a feed object
	def calculate_comments(self):
		# counts the total comments that apper on the page
		self.comments = Feed.objects.filter(parent=self).count()
		self.save()

		return self.comments


	def comment(self, user, post):
		# defines the user, his post and assigns the parent as self
		feed_comment = Feed(user=user, post=post, parent=self)
		feed_comment.save()

		self.comments = Feed.objects.filter(parent=self).count()

		self.save()
		return feed_comment

	# seriously, why?!!!
	def linkfy_post(self):
		return bleach.linkfy(escape(self.post))