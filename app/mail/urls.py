from django.urls import path

from mail.views import MailBoxAPIView, MailBoxFolders, MailMessageAPIView, MailBoxEventAPIView

urlpatterns = [
    path('api/v1/mail/', MailBoxAPIView.as_view()),
    path('api/v1/messages/', MailMessageAPIView.as_view()),
    path('api/v1/folders/', MailBoxFolders.as_view()),
    path('api/v1/event/', MailBoxEventAPIView.as_view())
]

