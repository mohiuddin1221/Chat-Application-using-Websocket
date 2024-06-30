from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroup
from .froms import ChatMessageCraeteForm

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_message.all()[:30]
    form = ChatMessageCraeteForm()
    if request.htmx:
        form = ChatMessageCraeteForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message' : message,
                'user' : request.user
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
    context = {
        'chat_messages': chat_messages,
        'form':form
    }
    return render(request, 'a_rtchat/chat.html', context)
