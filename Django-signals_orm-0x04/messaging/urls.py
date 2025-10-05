from django.urls import path
from .views import delete_user, send_message

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
     path('send/<int:receiver_id>/', send_message, name='send_message'),
    path('reply/<int:receiver_id>/<int:parent_id>/', send_message, name='reply_message'),
]
