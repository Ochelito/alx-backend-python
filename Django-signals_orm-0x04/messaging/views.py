from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, User
from django.contrib import messages
from django.shortcuts import render

@login_required
def send_message(request, receiver_id, parent_id=None):
    """
    Send a new message.
    Optional: parent_id for replying to a specific message.
    """
    if request.method == "POST":
        content = request.POST.get("content")
        if not content:
            messages.error(request, "Message cannot be empty.")
            return redirect("inbox")  # or wherever you want to redirect

        receiver = get_object_or_404(User, pk=receiver_id)

        # parent message (for threaded reply)
        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, pk=parent_id)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message
        )

        messages.success(request, "Message sent successfully!")
        return redirect("conversation", msg_id=parent_id or receiver_id)

    # If GET request, show form
    return render(request, "messaging/send_message.html", {"receiver_id": receiver_id})

@login_required
def inbox_view(request):
    """
    Show all messages for the logged-in user, including threaded replies.
    Optimized with select_related and prefetch_related.
    """
    # Fetch messages where the user is sender or receiver
    messages = (
        Message.objects.filter(receiver=request.user)
        .select_related('sender', 'receiver')         # avoid extra queries for FK
        .prefetch_related('replies__sender')         # fetch replies and their senders
        .order_by('-timestamp')
    )

    return render(request, "messaging/inbox.html", {"messages": messages})


@login_required
def unread_inbox_view(request):
    """
    Display unread messages for the logged-in user.
    Optimized with select_related and only() directly in the view.
    """
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .select_related('sender')  # avoid extra queries for sender FK
        .only('id', 'sender', 'content', 'timestamp', 'parent_message')  # fetch only necessary fields
    )
    
    return render(request, "messaging/unread_inbox.html", {"messages": unread_messages})

@login_required
def read_message_view(request, msg_id):
    message = Message.objects.select_related('sender').get(id=msg_id)
    if message.receiver == request.user and not message.read:
        message.read = True
        message.save(update_fields=['read'])  # only update the read field
    return render(request, "messaging/message_detail.html", {"message": message})
