import json

from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls.base import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from app import forms

from app.models import Chat, User, Event, Recipient, Idea


def home(request):
    if request.user.is_authenticated:
        events = Event.objects.exclude(members__id=request.user.id)
    else:
        events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, "app/home.html", context)

def sign_out(request):
    logout(request)
    return redirect('home')


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = forms.SigninForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data.get('user')
            if user:
                login(request, user)
                user.save()
                return redirect(request.GET.get('next') or 'home')
    context = {
        'form': form,
    }
    return render(request, 'registration/login.html', context)


def register(request):
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = forms.SignupForm()
    context = {
        "form": form,
    }
    return render(request, "registration/register.html", context)


def event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.POST.get("delete"):
        event.delete()
        return redirect("home")
    if request.POST.get("delete-contributor"):
        messages.success(request, "❌ Removed contributor.")
        event.members.remove(request.POST.get("delete-contributor"))
    add_recipient_form = forms.NewRecipientForm(event=event)
    context = {
        "event": event,
        "recipients": event.recipients.all(),
        "add_recipient_form": add_recipient_form,
        # "json": {
        #     "event_id": event.id,
        #     "contributors": [
        #         {
        #             "id": user.id,
        #             "first_name": user.first_name,
        #             "last_name": user.last_name,
        #             "username": user.username,
        #         }
        #         for user in event.members.all()
        #     ],
        # },
    }
    return render(request, "app/event.html", context)

@login_required
def event_recipients(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = forms.NewRecipientForm(request.POST, event=event)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.event = event
            recipient.save()
            form.save_m2m()
            messages.success(request, "😎 Successfully added recipient.")
    return redirect("event", event_id)

@login_required
def remove_event_recipient(request, event_id, recipient_id):
    get_object_or_404(Recipient, pk=recipient_id).delete()
    return redirect("event", event_id)

@login_required
def event_add_edit(request, pk=None):
    if pk:
        event = get_object_or_404(Event, pk=pk)
        if request.method == "POST":
            form = forms.EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "🗓 Event saved.")
                return redirect("event", event.id)
        else:
            form = forms.EventForm(instance=event)
    else:
        if request.method == "POST":
            form = forms.EventForm(request.POST)
            if form.is_valid:
                new_event = form.save(commit=False)
                new_event.organizer_id = request.user.id
                new_event.save()
                new_event.members.add(request.user)
                messages.success(request, "🗓 Event added.")
                return redirect("event", new_event.id)
        else:
            form = forms.EventForm()
    context = {"form": form}
    return render(request, "app/event_add_edit.html", context)

@login_required
def event_membership(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.members.filter(id=request.user.id).exists():
        if request.user == event.organizer:
            messages.error(
                request, "You are the organizer, you cannot leave this event."
            )
            return redirect("event", pk)
        event.members.remove(request.user)
        return redirect("home")
    else:
        event.members.add(request.user)
        return redirect("event", pk)


def event_membership_async(request, event_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    event = get_object_or_404(Event, pk=event_id)
    if event.members.filter(id=user_id).exists():
        if user == event.organizer:
            return HttpResponse(
                "You are the organizer, you cannot leave this event.", status=403
            )
        event.members.remove(user)
        return HttpResponse(status=200)
    else:
        event.members.add(user)
        return HttpResponse(status=200)


@login_required
def recipient(request, event_id, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    ideas = recipient.ideas.select_related("creator").order_by('-id')

    context = {"recipient": recipient, "ideas": ideas}
    return render(request, "app/recipient.html", context)

@login_required
def idea(request, event_id, recipient_id, pk):
    idea = get_object_or_404(Idea, pk=pk)
    context = {"idea": idea}
    return render(request, "app/idea.html", context)

@login_required
def idea_add_edit(request, event_id, recipient_id, pk=None):
    idea = None

    if pk:
        idea = get_object_or_404(Idea, pk=pk)
        if request.method == "POST":
            form = forms.IdeaForm(request.POST, instance=idea)
            if form.is_valid():
                form.save()
                messages.success(request, "💡 Idea saved.")
                return redirect("recipient", event_id, recipient_id)
        else:
            form = forms.IdeaForm(instance=idea)
    else:
        if request.method == "POST":
            form = forms.IdeaForm(request.POST)
            if form.is_valid:
                new_idea = form.save(commit=False)
                new_idea.creator = request.user
                new_idea.recipient_id = recipient_id
                new_idea.save()
                messages.success(request, "💡 Idea added.")
                return redirect("recipient", event_id, recipient_id)
        else:
            form = forms.IdeaForm()

    context = {
        "idea": idea,
        "form": form,
        "back": reverse("recipient", args=[event_id, recipient_id]),
    }
    return render(request, "app/idea_add_edit.html", context)

@login_required
def like_idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    return redirect("idea", idea.recipient.event.id, idea.recipient.id, idea_id)


def chat(request, pk):
    if request.method == "POST":
        body = json.loads(request.body)
        print(body)
        c = Chat.objects.create(
            user=request.user, group_id=pk, content=body.get("content")
        )
        return JsonResponse(c.serialize())
    if request.method == "GET":
        chats = Chat.objects.filter(group_id=pk).order_by("-id").select_related("user")
        return JsonResponse({"data": [c.serialize() for c in chats]})
    return Http404


# flag auto-add recipient when they join the group
# later add support for unsuspecting recipient
#
