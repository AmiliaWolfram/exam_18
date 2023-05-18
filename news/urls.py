from django.urls import path

from news.views import NewsListCreateView, NewsRetrieveUpdateDestroyAPIView, \
    CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView, \
    StatusListCreateAPIView, StatusRetrieveUpdateDestroyView, \
    NewsStatusListView, CommentStatusListView


urlpatterns = [
    path('news/', NewsListCreateView.as_view()),
    path('news/<int:pk>', NewsRetrieveUpdateDestroyAPIView.as_view()),
    path('news/<int:news_id>/comments/', CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('statuses/', StatusListCreateAPIView.as_view()),
    path('statuses/<pk>/', StatusRetrieveUpdateDestroyView.as_view()),
    path('news/<int:pk>/<str:slug>/', NewsStatusListView.as_view()),
    path('news/<int:news_id>/comments/<int:comment_id>/<str:slug>/', CommentStatusListView.as_view()),
]
