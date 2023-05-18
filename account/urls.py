from django.urls import path

from account.views import AuthorRegisterAPIView, MyObtainAuthToken

urlpatterns = [
    path('account/register/', AuthorRegisterAPIView.as_view()),
    path('account/token/', MyObtainAuthToken.as_view()),
]
