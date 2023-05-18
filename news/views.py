from django.shortcuts import get_object_or_404
from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from account.models import Author
from news.models import News, Comment, Status, NewsStatus, CommentStatus
from news.permissions import IsAuthorOrIsAuthenticated
from news.serializers import NewsSerializer, CommentSerializer, StatusSerializer, \
    NewsStatusSerializer, CommentStatusSerializer


from django.contrib.auth import authenticate, login
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Вход выполнен успешно'})
        else:
            return JsonResponse({'error': 'Неверное имя пользователя или пароль'}, status=400)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=400)


class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        author_id = request.data.get('author_id')

        author = None
        if author_id:
            author = get_object_or_404(Author, id=author_id)

        news = News(title=title, content=content, author=author)
        news.save()

        serializer = NewsSerializer(news)

        return Response(serializer.data)


class NewsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['pk'])


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrIsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['news_id'])


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrIsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs['news_id'])


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]


class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser]


class NewsStatusListView(generics.ListAPIView):
    queryset = NewsStatus.objects.all()
    serializer_class = NewsStatusSerializer

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        slug = self.kwargs['slug']
        queryset = News.objects.filter(id=news_id, slug=slug)
        return queryset

    def perform_create(self, serializer):
        news_id = self.kwargs['news_id']
        if self.request.user == News.objects.get(id=news_id).author:
            serializer.save(news_id=news_id)
            return Response({'message': 'Статус новости успешно добавлен'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Вы не являетесь автором данной новости'}, status=status.HTTP_403_FORBIDDEN)


class CommentStatusListView(generics.ListAPIView):
    queryset = CommentStatus.objects.all()
    serializer_class = CommentStatusSerializer

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        if self.request.user == Comment.objects.get(id=comment_id).author:
            serializer.save(comment_id=comment_id)
            return Response({'message': 'Статус комментария успешно добавлен'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Вы не являетесь автором данной новости'}, status=status.HTTP_403_FORBIDDEN)
