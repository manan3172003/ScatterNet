from rest_framework import serializers
from django.contrib.auth.models import User
from dodgerblue.settings import NODEHOSTNAME
from .models import Author
from hashlib import sha256

class AuthorSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_node = serializers.BooleanField(default=False)

    class Meta:
        model = Author
        fields = ('username', 'password', 'displayName', 'host', 'github', 'profileImage', 'page', 'is_node')
        #this will also need to be cleaned up later when we finalize the host stuff
        extra_kwargs = {
            'host': {'required': False, 'allow_null': True},
            'github': {'required': False, 'allow_null': True},
            'profileImage': {'required': False, 'allow_null': True},
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

        author.id_url = "{}/api/authors/{}".format(NODEHOSTNAME, author.id)
        author.host = NODEHOSTNAME
        author.page = "{}/authors/{}".format(NODEHOSTNAME, author.id)
        author.save()

        return author

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField(read_only=True)
    state = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    serial = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Author
        fields = ('serial', 'type', 'id', 'host', 'displayName', 'github', 'profileImage', 'page', 'state', 'username')

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "author"

    def get_serial(self, obj):
        return obj.id

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
        fields = ('type', 'id', 'username', 'host', 'displayName', 'github', 'profileImage', 'page', 'state')
        extra_kwargs = {
            'displayName': {'required': False}, #not necessary to update it p much
            'state': {'required': False} #so users can also update other stuff
        }

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "author"

class RemoteAuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    serial = serializers.SerializerMethodField(read_only=True)
    id = serializers.URLField()

    class Meta:
        model = Author
        fields = ('serial', 'type', 'id', 'host', 'displayName', 'github', 'profileImage', 'page')

    def create(self, validated_data):
        author = Author.objects.create(
            id_url=validated_data.get('id'),
            host=validated_data.get('host'),
            displayName=validated_data.get('displayName'),
            github=None,
            profileImage=validated_data.get('profileImage'),
            page=validated_data.get('page'),
            is_local=False,
            state='ACTIVE',
            username=sha256(validated_data.get('id').encode('utf-8')).hexdigest()
        )
        author.save()

        return author

    def update(self, instance, validated_data):
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id_url
        return data

    def get_serial(self, obj):
        return obj.id

    def get_type(self, obj):
        return "author"