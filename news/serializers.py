from django.db import IntegrityError
from rest_framework import serializers, generics
from rest_framework.exceptions import ValidationError

from news.models import News, Status, Comment, NewsStatus, CommentStatus


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = News
        fields = ['title', 'content', 'author']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            new_reaction_type = validated_data.pop('reaction')
            instance = self.Meta.model.objects.get(**validated_data)
            instance.reaction = new_reaction_type
            instance.save()
            return instance


class NewsStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsStatus
        fields = ['news']


class CommentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentStatus
        fields = ['comment']
