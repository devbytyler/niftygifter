import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from multiavatar.multiavatar import multiavatar

# Create your models here.

class User(AbstractUser):
    '''
    Extends AbstractUser, already has these fields
    username
    first_name
    last_name
    email
    password
    is_superuser()
    is_authenticated()
    '''
    avatar_seed = models.UUIDField(null=True)
    @property
    def avatar(self):
        return multiavatar(self.avatar_seed or self.username, None, None)

    def regenerate_avatar(self):
        self.avatar_seed = uuid.uuid4()
        self.save()
    
    def reset_avatar(self):
        self.avatar_seed = None
        self.save()


class Event(models.Model):
    title = models.CharField(max_length=100)
    exchange_date = models.DateField(auto_now=False, auto_now_add=False)
    organizer = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="memberships")
    # code
    # cover_image
    # is_public

    # Event Members
    '''
    - See a list of members (organizer can remove). If also recipient, recipient not deleted.
    - Option to invite a member by email. Clicking email auto joins group.
    - See a list of recipients. Some are members. Organizer can remove recipients.
    - If a member-recipient leaves a group, they will still be associated with the recipient in case they join again.
    - Organizer can add recipients, either from list of members, or create Non-Member list.
    '''

class Recipient(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="recipients", blank=True)
    blocked_users = models.ManyToManyField(User, related_name="block_recipients", blank=True)
    decider = models.ForeignKey(User, related_name="decisions", on_delete=models.SET_NULL, null=True, blank=True)

    '''
    How does a recipient get added?
    - Admin can make a member that joined into a recipient.
    - Admin can invite a member to the group, making them a member or not.
    - Admin can create an external member 
    '''

class Notification(models.Model):
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    recipient = models.ForeignKey(Recipient, related_name='ideas', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    notifications = GenericRelation(Notification)
    price = models.FloatField(default=0.0)
    selected = models.BooleanField(default=False)

class Chat(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name='chats', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Recipient, related_name='chats', on_delete=models.CASCADE)
    notifications = GenericRelation(Notification)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at,
            "user": self.user.get_full_name(),
            "user_id": self.user.id,
            "user_avatar": self.user.avatar,
        }

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


'''
[NO] Anybody in the group can create a gift for anybody else in the group.
[NO] A recipient can be added twice to an event.
[YES] Many ideas can be added to a recipient, several can be selected for purchase.
[YES] A recipient can only have one decider.
[YES] Deciders must belong to the group.
[YES] Organizers assign deciders.
'''