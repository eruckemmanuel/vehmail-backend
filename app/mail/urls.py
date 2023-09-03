from django.urls import path

from mail.views import MailBoxAPIView, MailBoxFolders

urlpatterns = [
    path('api/v1/mail/', MailBoxAPIView.as_view()),
    path('api/v1/folders/', MailBoxFolders.as_view())
]

