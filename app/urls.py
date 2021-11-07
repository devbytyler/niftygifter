from django.urls import include, path

from . import views

urlpatterns = [
    # Accounts
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register, name='register'),

    # Events
    path('events/new', views.event_add_edit, name='event_new'),
    path('events/<int:pk>', views.event, name='event'),
    path('events/<int:pk>/edit', views.event_add_edit, name='event_edit'),
    path('events/<int:pk>/membership/', views.event_membership, name='event_membership'),
    path('events/<int:event_id>/recipients/', views.event_recipients, name='event_recipients'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/remove', views.remove_event_recipient, name='event_recipients_remove'),
    path('async/events/<int:event_id>/membership/<int:user_id>', views.event_membership_async, name='event_membership_async'),

    # Recipients
    path('events/<int:event_id>/recipients/<int:pk>', views.recipient, name='recipient'),
    path('async/recipients/<int:pk>/chat', views.chat, name='recipient_chat'),

    # Ideas
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/new', views.idea_add_edit, name='idea_new'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/<int:pk>', views.idea, name='idea'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/<int:pk>/edit', views.idea_add_edit, name='idea_edit'),
    path('ideas/<int:idea_id>/like', views.like_idea, name='like_idea'),


]