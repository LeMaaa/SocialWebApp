from __future__ import unicode_literals
from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    posts_title = models.CharField(max_length=100)
    posts_content = models.TextField(max_length =160)
    user = models.ForeignKey(User)   
    post_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.posts_content 

class UserProfile(models.Model):
    email = models.CharField(blank=True, max_length=32)
    user = models.OneToOneField(User,related_name='userprofile')
    picture = models.FileField(upload_to="images", blank=True)
    content_type = models.CharField(max_length=50,)
    bio = models.TextField(max_length=500, blank=True)
    userage = models.IntegerField(null = True, blank = True)
    ip_addr = models.GenericIPAddressField()
    friends = models.ManyToManyField(User, related_name = 'friends')
    # friendships = models.ManyToManyField(Friendship,related_name = 'friendships')

    def __unicode__(self):
        return self.content_type

class Comment(models.Model):
    comment_content = models.TextField()
    comment_post = models.ForeignKey(Posts)
    comment_time = models.DateTimeField(auto_now_add=True, editable=False)
    comment_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.reply_content

# class Friendship(models.Model):
#     user_follow_friend = models.BooleanField(default=False)
#     friend_follow_user = models.BooleanField(default=False)
#     user = models.ForeignKey(User, related_name='owner_user')
#     friend = models.ForeignKey(User, related_name='friend_user', null=True)

#     def __unicode__(self):
#         return self.user.username + self.friend.username 