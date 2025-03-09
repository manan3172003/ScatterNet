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

        author.id_url = "http://localhost:8000/api/authors/{}".format(author.id)
        author.page = "http://localhost:8000/authors/{}".format(author.id)
        author.save()

        return author

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField(read_only=True)
    state = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName', 'github', 'profileImageURL', 'page', 'state', 'username')

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "author"

    #overrides conditional representation, we remove the state if it isnt a node admin requesting it
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)
        # if no request or user is not node admin, remove the state field
        if not request or request.user.is_staff == False:
            representation.pop('state', None)
            representation.pop('username', None)
        return representation

class AuthorUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    page = serializers.URLField(read_only=True)

    class Meta:
        model = Author
        fields = ('type', 'id', 'username', 'host', 'displayName', 'github', 'profileImageURL', 'page', 'state')
        extra_kwargs = {
            'displayName': {'required': False}, #not necessary to update it p much
            'state': {'required': False} #so users can also update other stuff
        }

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "author"
