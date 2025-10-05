from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # triggers post_delete signals
    messages.success(request, "Your account has been deleted successfully.")
    return redirect("home")  # change "home" to your landing page
