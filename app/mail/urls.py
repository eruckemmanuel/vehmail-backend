from django.urls import path

from mail.views.rest.mails import ListMailAPIView, MailBoxFolders, MailMessageAPIView
from mail.views.rest.events import MailBoxEventAPIView

urlpatterns = [
    path('api/v1/mail/', ListMailAPIView.as_view()),
    path('api/v1/messages/', MailMessageAPIView.as_view()),
    path('api/v1/folders/', MailBoxFolders.as_view()),
    path('api/v1/event/<str:event_token>', MailBoxEventAPIView.as_view())
]

