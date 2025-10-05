from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, User
from django.contrib import messages

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
