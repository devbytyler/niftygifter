from django.db import models
from django.contrib.auth.models import AbstractUser

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
    pass

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

class Idea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    recipient = models.ForeignKey(Recipient, related_name='ideas', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # price = models.FloatField(default=0.0)
    # link = models.CharField(max_length=200, blank=True, default='')
    # likers = models.ManyToManyField(User, related_name='likes')
    # selected
    # image

class Chat(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name='chats', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Recipient, related_name='chats', on_delete=models.CASCADE)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at,
            "user": self.user.get_full_name(),
            "user_id": self.user.id
        }


'''

class Comment(models.Model):
    text
    user
    idea
    event? Meaning comments for the whole event, not specific to a certain idea
    pass

class Notification(model):
    read
    entity
    user
'''

'''
[NO] Anybody in the group can create a gift for anybody else in the group.
[NO] A recipient can be added twice to an event.
[YES] Many ideas can be added to a recipient, several can be selected for purchase.
[YES] A recipient can only have one decider.
[YES] Deciders must belong to the group.
[YES] Organizers assign deciders.
'''