from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# 
# Why?
from django.utils.html import escape

@python_2_unicode_compatible
class Activity(models.Model):
	# 
	# Defining the array
	FAVOURITE = 'F'
	LIKE = 'L'
	UP_VOTE = 'U'
	DOWN_VOTE = 'D'
	ACTIVITY_ROLES = (
		(FAVOURITE, "favourite"),
		(LIKE, "like"),
		(UP_VOTE, 'Up Vote'),
		(DOWN_VOTE, "Down Vote"),
		)		

	user = models.ForeignKey(User)
	activity_type = models.CharField(max_length=1, choices=ACTIVITY_ROLES)
	date = models.DateTimeField(auto_now_add=True)
	feed = models.IntegerField(null=True, blank=True)
	# Only usable when the QnA app is made
	question = models.IntegerField(null=True, blank=True)
	answer = models.IntegerField(null=True, blank=True)


	class Meta:
		verbose_name= 'Activity'
		verbose_name_plural= 'Activities'


	def __str__(self):
		return self.activity_type


# 
#  To be done only when doing notification

# @python_2_unicode_compatible
# class Notification(models.Model):
# 	LIKED = 'L'
# 	COMMENTED = 'C'
# 	FAVOURITED = 'F'
# 	ANSWERED = 'A'
# 	ACCEPTED_ANSWER = 'W'
# 	