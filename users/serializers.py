from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    detail_url = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile_picture', 'is_artist', 'detail_url','profile_picture_url')
        read_only_fields = ['profile_picture_url']

    
    
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None
    
    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            # Check if the user is an artist and return the appropriate URL
            if obj.is_artist:
                return request.build_absolute_uri(
                    reverse('artist-profile', kwargs={'pk': obj.pk})
                )
            else:
                return request.build_absolute_uri(
                    reverse('user-profile', kwargs={'pk': obj.pk})
                )
        return None

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class MiniUserSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()    
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_picture', 'is_artist', 'detail_url','profile_picture_url')
        read_only_fields = ['profile_picture_url']
        
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None
    
    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            # Check if the user is an artist and return the appropriate URL
            if obj.is_artist:
                return request.build_absolute_uri(
                    reverse('artist-profile', kwargs={'pk': obj.pk})
                )
            else:
                return request.build_absolute_uri(
                    reverse('user-profile', kwargs={'pk': obj.pk})
                )
        return None
