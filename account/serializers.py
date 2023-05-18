from rest_framework import serializers, generics
from rest_framework.exceptions import ValidationError

from account.models import Author, User


class AuthorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)
    password2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2",
                  "first_name", "last_name", "age"]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        if data['password'].isdigit():
            raise serializers.ValidationError("Password must contain letters")
        if not any(char.isupper() for char in data['password']) or not any(char.islower() for char in data['password']):
            raise serializers.ValidationError("Password must contain both uppercase and lowercase letters")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age']
        )
        user.set_password(validated_data['password'])
        user.save()
        try:
            author = Author.objects.create(user=user)
        except Exception as e:
            user.delete()
            raise e
        else:
            author.username = user.username
            author.age = user.age
        return author
