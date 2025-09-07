from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



class CustomUserSerializer(serializers.ModelSerializer):
    #bio = serializers.CharField()
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', 'email', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    
    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value
    
    def create(self, validated_data):
        # Ensure 'email' and 'bio' are handled correctly
        email = validated_data.get('email')
        bio = validated_data.get('bio', '')  # Default to empty string if bio is not provided

        if not email:
            raise serializers.ValidationError("Email is required.")

        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email,
            bio=bio,
            profile_picture=validated_data.get('profile_picture', None),
        )
        Token.objects.create(user=user)
        return user