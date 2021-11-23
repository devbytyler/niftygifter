from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from app.forms import SigninForm

from . import views

urlpatterns = [
    # Accounts
    path('', views.home, name='home'),
    path('accounts/login/', views.sign_in, name='login'),
    path('accounts/logout/', views.sign_out, name='logout'),
    # path('login/', views.sign_in, name='login'),
    path('accounts/register/', views.register, name='register'),

    # Events
    path('events/new', views.event_add_edit, name='event_new'),
    path('events/<int:pk>', views.event, name='event'),
    path('events/<int:pk>/edit', views.event_add_edit, name='event_edit'),
    path('events/<int:pk>/membership/', views.event_membership, name='event_membership'),
    path('async/events/<int:event_id>/membership/<int:user_id>', views.event_membership_async, name='event_membership_async'),

    # Recipients
    path('events/<int:event_id>/recipients/', views.recipients_add_edit, name='event_recipients'),
    path('events/<int:event_id>/recipients/<int:recipient_id>', views.recipient_ideas, name='recipient_ideas'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/edit', views.recipients_add_edit, name='event_recipients_edit'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/remove', views.remove_event_recipient, name='event_recipients_remove'),
  
    # Ideas
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/new', views.idea_add_edit, name='idea_new'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/<int:pk>', views.idea, name='idea'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/<int:pk>/edit', views.idea_add_edit, name='idea_edit'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/<int:pk>/delete', views.idea_delete, name='idea_delete'),
    path('events/<int:event_id>/recipients/<int:recipient_id>/ideas/<int:pk>/like', views.idea_like, name='idea_like'),

    #async
    path('async/recipients/<int:pk>/chat', views.chat, name='recipient_chat'),


]