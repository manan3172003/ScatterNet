from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author

class AuthorSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = ('username', 'password', 'displayName', 'host', 'github', 'profileImageURL', 'page')
        #this will also need to be cleaned up later when we finalize the host stuff
        extra_kwargs = {
            'host': {'required': False, 'allow_null': True},
            'github': {'required': False, 'allow_null': True},
            'profileImageURL': {'required': False, 'allow_null': True},
            'page': {'required': False, 'allow_null': True},
        }

        #serializers provide field level validation, where you just validate_fieldname and it does it automatically
        # during is_valid() - ref: https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
        def validate_username(self, value):
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("A user with this provided username already exists.")
            return value

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.pop('password')
        created_user = User(username=username)
        created_user.set_password(password)
        created_user.save()

        author = Author.objects.create(
            user=created_user,
            state='PENDING', #by default, we'll keep it pending until accepted by node admin
            is_local=True,
            **validated_data)
        return author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'github', 'profileImageURL', 'page')
